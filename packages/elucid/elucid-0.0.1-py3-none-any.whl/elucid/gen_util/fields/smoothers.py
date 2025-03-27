from __future__ import annotations
import numpy as np
from numba import njit, int64, float64, prange
from numba.experimental import jitclass
from pyhipp.core import abc, dataproc as dp
from .periodic import PeriodicField
from ..fft import FFTPolicy, default_fft_policy

class Smoother(abc.HasDictRepr, abc.HasLog):
    
    Field = PeriodicField
    
    def run(self, field: Field) -> Field:
        '''
        @field: has to be density contrast field.
        '''
        raise NotImplementedError()
    
    @property
    def volume(self) -> float:
        raise NotImplementedError()

class TopHatSmoother(Smoother):
    
    Field = Smoother.Field    
    repr_attr_keys = 'r', 'filter_shape'
    
    def __init__(self, r: float, filter_shape='cubic', **kw) -> None:
        super().__init__(**kw)
        
        assert filter_shape in ('cubic', )
        
        self.r = r
        self.filter_shape = filter_shape
        
    @property
    def volume(self) -> float:
        return (2.0*self.r) ** 3
        
    def run(self, field: Field):
        return self.__run_cubic(field)
        
    def __run_cubic(self, field: Field):
        ccfg, data = field.cell_cfg, field.data
        l_grid, n_grids = ccfg.l_grid, ccfg.n_grids
        
        n_sm = int(np.ceil(self.r / l_grid))
        assert n_sm < n_grids
        self.log(f'Running with cubic filter, l={self.r}, '
                 f'using {n_sm} neighbors')

        data_out = np.empty_like(data)
        self.__run_cubic_impl(data, n_sm, data_out)
        return TopHatSmoother.Field(data=data_out, cell_cfg=ccfg)
     
    @staticmethod
    def __run_cubic_impl(data: np.ndarray, n_sm: int, data_out: np.ndarray):
        n = data.shape[0]
        scale = 1.0 / (2 * n_sm + 1) ** 3
        for i0 in range(n):
            for i1 in range(n):
                for i2 in range(n):
                    x_all = 0.
                    for d0 in range(-n_sm, n_sm+1):
                        for d1 in range(-n_sm, n_sm+1):
                            for d2 in range(-n_sm, n_sm+1):
                                _i0 = (i0 + d0) % n
                                _i1 = (i1 + d1) % n
                                _i2 = (i2 + d2) % n
                                x_all += data[_i0,_i1,_i2]
                    data_out[i0,i1,i2] = x_all * scale
                    
class FFTTopHatSmoother(Smoother):
    
    Field = Smoother.Field

    repr_attr_keys = 'r'

    def __init__(self, r: float, fft_pl: FFTPolicy = default_fft_policy, 
                 **kw) -> None:
        
        super().__init__(**kw)
        
        self.r = r
        self.fft_pl = fft_pl
        
    @property
    def volume(self) -> float:
        return 4./3. * np.pi * self.r ** 3
    
    def run(self, field: Field) -> Field:
        fft_pl = self.fft_pl
        f_in_k = field.fft(fft_pl)
        return self.run_from_k_space(f_in_k)
    
    def run_from_k_space(self, f_in_k: Field) -> Field:
        fft_pl = self.fft_pl
        ccfg = f_in_k.cell_cfg
        l, l_box, n = self.r, ccfg.l_box, ccfg.n_grids
        k_scale = 2.0 * np.pi * l / l_box
        n_z = n // 2 + 1
        
        assert f_in_k.shape == (n, n, n_z)
        self.__mul_filter_in_k(f_in_k.data, k_scale)
        f_in_x = f_in_k.ifft(fft_pl)
        
        data = f_in_x.data
        norm = data.mean()
        data /= norm
        if np.abs(norm - 1.) > 1.0e-2:
            self.log(f'Normalized real space field by {norm}')
        
        return f_in_x
    
    @staticmethod
    @njit
    def __mul_filter_in_k(f_in_k: np.ndarray, k_scale: float):
        n0, n1, n2 = f_in_k.shape
        n_half = n0 // 2
        for i0 in prange(n0):
            _i0 = np.float64(i0 if i0 < n_half else i0 - n0)
            for i1 in range(n1):
                _i1 = np.float64(i1 if i1 < n_half else i1 - n1)
                for i2 in range(n2):
                    _i2 = np.float64(i2)
                    if i0 == i1 == i2 == 0:
                        continue
                    kl = np.sqrt(_i0*_i0 + _i1*_i1 + _i2*_i2) * k_scale
                    kl3 = kl*kl*kl
                    w = 3.0 * (np.sin(kl) - kl * np.cos(kl)) / kl3
                    f_in_k[i0, i1, i2] *= w

class FFTMassAdaptiveSmoother(Smoother):
    
    Field = Smoother.Field
    repr_attr_keys = 'mean_density', 'target_mass', 'lagrangian_r', \
        'dr_rel', 'dr_abs', 'r_max', 'fft_pl'
    
    def __init__(self, mean_density, target_mass, 
        dr_rel = 0.2, dr_abs = 0.1, r_max = 32.0,
        fft_pl: FFTPolicy = default_fft_policy, **kw) -> None:
        
        super().__init__(**kw)
        
        r3 = target_mass / (4.0/3.0*np.pi*mean_density)
        r = r3**(1./3.)
        
        self.mean_density = mean_density
        self.target_mass = target_mass
        self.lagrangian_r = r
        self.dr_rel = dr_rel
        self.dr_abs = dr_abs
        self.r_max = r_max
        self.fft_pl = fft_pl
        
    def run(self, field: Field) -> Field:
        ccfg = field.cell_cfg
        r, dr_rel, dr_abs, r_max = ccfg.l_grid, self.dr_rel, \
            self.dr_abs, self.r_max
        
        self.log(f'Start smoothing with {r=}')
        f_in_k = field.fft(self.fft_pl)
        out_f = self.__get_smoothed(f_in_k, r)
        c = self.__chk_convergence(out_f, r, None)
        left_idx = (c < 0.0).nonzero()[0]
        c = c[left_idx]
        
        while left_idx.size > 0:
            next_r = max(r*(1.+dr_rel), r + dr_abs)
            if next_r > r_max:
                self.log(f'r ({next_r}) > maximal r ({r_max}). Iteration ends.')
                break
            self.log(f'Try {r=} for {left_idx.size} grids, mean mass ratio '
                     f'= {c.mean()}')
            next_f = self.__get_smoothed(f_in_k, next_r)
            next_c = self.__chk_convergence(next_f, next_r, left_idx)
            left_idx, c = self.__update_field(
                out_f, next_f, left_idx, c, next_c)
            r = next_r

        data = out_f.data
        norm = data.mean()
        data /= norm
        if np.abs(norm - 1.) > 1.0e-2:
            self.log(f'Normalized real space field by {norm}')

        return out_f

    def __get_smoothed(self, f_in_k: Field, r: float):
        s = FFTTopHatSmoother(r, fft_pl=self.fft_pl, verbose=self.verbose)
        return s.run_from_k_space(f_in_k)
    
    def __chk_convergence(self, f_in_x: Field, r: float, idx: np.ndarray):
        d_target = self.target_mass / ( 
            4.0 / 3.0 * np.pi * r ** 3 * self.mean_density)
        d = f_in_x.data.ravel()
        if idx is not None:
            d = d[idx]
        c = dp.Num.safe_lg(d / d_target)
        return c

    @staticmethod
    def __update_field(f: Field, next_f: Field, idx: np.ndarray, 
            c: np.ndarray, next_c: np.ndarray):
        d, next_d = f.data.ravel(), next_f.data.ravel()
        left = next_c < 0.0
        conv = ~left
        conv_idx, left_idx = idx[conv], idx[left]
        
        # make interpolation for the converged
        y, next_y = dp.Num.safe_lg(d[conv_idx], next_d[conv_idx]) 
        x, next_x = c[conv], next_c[conv]
        dy, dx = next_y - y, next_x - x
        assert (x < 0.0).all()
        assert (dx > 0.0).all()
        interp_y = dy / dx * (-x) + y
        d[conv_idx] = 10.0**interp_y
        
        d[left_idx] = next_d[left_idx]
    
        return left_idx, next_c[left]

@jitclass
class _MassAdaptiveSmootherCubic:
    
    data: float64[:, :, :]
    rho_sum: float64
    data_out: float64[:, :, :]
    n: int64
    
    def __init__(self, data: np.ndarray, rho_sum: float, 
                 data_out: np.ndarray) -> None:
        self.data = data
        self.rho_sum = rho_sum
        self.data_out = data_out
        self.n = data.shape[0]
        
    def run(self):
        data_out, n = self.data_out, self.n
        for i0 in range(n):
            for i1 in range(n):
                for i2 in range(n):
                    i_3d = np.array((i0, i1, i2))
                    data_out[i0, i1, i2] = self.__rho_at(i_3d)
    
    def __rho_at(self, i_3d: np.ndarray):
        data, rho_sum, n = self.data, self.rho_sum, self.n
        rho_all, n_sm = 0.0, 0
        while True:
            for d0 in range(-n_sm, n_sm+1):
                for d1 in range(-n_sm, n_sm+1):
                    for d2 in range(-n_sm, n_sm+1):
                        d_3d = np.array((d0, d1, d2))
                        if (np.abs(d_3d) < n_sm).all():
                            continue
                        i0, i1, i2 = (i_3d + d_3d) % n
                        rho_all += data[i0, i1, i2]
            if rho_all >= rho_sum:
                break
            n_sm += 1
        scale = 1.0 / (2 * n_sm + 1) ** 3
        return rho_all * scale

class MassAdaptiveSmoother(Smoother):
    
    Field = Smoother.Field
    repr_attr_keys = 'mass', 'filter_shape'
    
    def __init__(self, mass: float, filter_shape='cubic', 
                 ensure_mass_conservetive = True,
                 **kw) -> None:
        super().__init__(**kw)
        
        assert filter_shape in ('cubic', )
        
        self.mass = mass
        self.filter_shape = filter_shape
        self.ensure_mass_conservetive = ensure_mass_conservetive
        
    def run(self, field: Field):
        ccfg, data = field.cell_cfg, field.data
        l_grid = ccfg.l_grid
        vol_cell = l_grid**3
        rho_sum = self.mass / vol_cell
        
        data_out = np.empty_like(data)
        _MassAdaptiveSmootherCubic(data, rho_sum, data_out).run()
        if self.ensure_mass_conservetive:
            data_out /= data_out.mean()
        return MassAdaptiveSmoother.Field(data=data_out, cell_cfg=ccfg)
        
        
