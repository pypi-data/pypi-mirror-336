from __future__ import annotations
from .non_periodic import NonPeriodicField, NonPeriodicCIC
from pyhipp.core import abc, dataproc as dp
import numpy as np
import numba
import typing
from ..fft import FFTPolicy, default_fft_policy
if typing.TYPE_CHECKING:
    from .smoothers import Smoother

class CellConfig(abc.HasDictRepr):
    
    repr_attr_keys = ('n_grids', 'l_box', 'l_grid')
    
    def __init__(self, n_grids: int, l_box: float, **kw) -> None:
        super().__init__(**kw)
        
        self.n_grids = n_grids
        self.l_box = l_box
        self.l_grid = l_box / n_grids
        self.dims = (n_grids, n_grids, n_grids)
        
    @property
    def tot_n_grids(self):
        return self.n_grids ** 3
        
    def shift_x_in(self, x: np.ndarray) -> None:
        l_box = self.l_box
        x[ x >= l_box ] -= l_box
        x[ x < 0.0 ] += l_box
        
    def shift_dx(self, dx: np.ndarray) -> None:
        l_box = self.l_box
        l_half = .5 * l_box
        dx[ dx >= l_half ] -= l_box
        dx[ dx < -l_half ] += l_box
        
    def shift_x_to(self, x: np.ndarray, x_dst: np.ndarray) -> None:
        dx = x - x_dst
        self.shift_dx(dx)
        x[...] = x_dst + dx
        
    def shift_cid_in(self, cid: np.ndarray) -> None:
        n_grids = self.n_grids
        np.putmask(cid, cid < 0, cid + n_grids)
        np.putmask(cid, cid >= n_grids, cid - n_grids)
    
    def x_to_cid_no_shift(self, x: np.ndarray):
        l_grid = self.l_grid
        id = np.floor(x / l_grid).astype(int)
        return id
        
    def x_to_cid(self, x: np.ndarray) -> np.ndarray:
        id = self.x_to_cid_no_shift(x)
        n_grids = self.n_grids
        np.putmask(id, id < 0, id + n_grids)
        np.putmask(id, id >= n_grids, id - n_grids)
        return id
    
    def cid_3d_to_1d(self, cid_3d: np.ndarray) -> np.ndarray:
        ndim = cid_3d.ndim
        assert ndim in (1,2)
        if cid_3d.ndim == 2:
            cid_3d = cid_3d.T
        return np.ravel_multi_index(tuple(cid_3d), self.dims)
    
    def cid_1d_to_3d(self, cid_1d: np.ndarray):
        cid = np.unravel_index(cid_1d, self.dims)
        cid = np.array(cid)
        if cid.ndim == 2:
            cid = cid.T
        return cid
    
    def test_bound_x(self, x: np.ndarray):
        return dp.frame.PeriodicBox.test_bound(x, l_box=self.l_box)
    
    def test_bound_cid(self, cid_3d: np.ndarray):
        return ((cid_3d >= 0)&(cid_3d < self.n_grids)).all()
    
    def test_bound_rect(self, x: np.ndarray, x_range: np.ndarray):
        x_lb, x_ub = np.asarray(x_range).T
        x_cent, x_span = .5*(x_lb + x_ub), .5*(x_ub - x_lb)
        dx = x - x_cent
        self.shift_dx(dx)
        return (np.abs(dx) <= x_span).all(1)
    
class PeriodicField(NonPeriodicField):
    
    repr_attr_keys = NonPeriodicField.repr_attr_keys + ('cell_cfg',)
    
    Shape = NonPeriodicField.Shape
    DType = NonPeriodicField.DType
    Axes = NonPeriodicField.Axes
    
    def __init__(self, data: np.ndarray, 
                 spatial_n_dims: int = 3, 
                 cell_cfg: CellConfig = None,
                 **kw) -> None:
        
        super().__init__(data, spatial_n_dims, **kw)

        self.bind_cell_cfg(cell_cfg)

    @classmethod
    def from_cell_cfg(cls, cell_cfg: CellConfig, dtype: DType = np.float64,
                      fill = 0, **init_kw):
        '''
        @init_kw: such as spatial_n_dims.
        '''
        shape = cell_cfg.dims
        return cls.from_shape(shape, dtype=dtype, fill=fill, 
                              cell_cfg=cell_cfg, **init_kw)
        
    def replaced_data(self, data: np.ndarray, **init_kw):
        return PeriodicField(data=data, spatial_n_dims=self.spatial_n_dims, 
                             cell_cfg=self.cell_cfg, **init_kw)

    def copied_data(self, **init_kw):
        return self.replaced_data(self.data.copy(), **init_kw)

    def bind_cell_cfg(self, cell_cfg: CellConfig = None):
        self.cell_cfg = cell_cfg
        
    def smoothed(self, smoother: Smoother):
        return smoother.run(self)
        
    def adapt_fft_policy(self, pl: FFTPolicy = default_fft_policy):
        if pl.axes is None and self.n_dims != self.spatial_n_dims:
            pl = pl.replaced(axes=self.spatial_axes)
        return pl
           
    def fft(self, pl: FFTPolicy = default_fft_policy):
        data_out = self.adapt_fft_policy(pl).forward(self.data)
        return self.replaced_data(data_out)
        
    def ifft(self, pl: FFTPolicy = default_fft_policy):
        data_out = self.adapt_fft_policy(pl).backward(self.data)
        return self.replaced_data(data_out)
           
class MassAssigner(abc.HasDictRepr, abc.HasLog):
    
    kind: str = None
    
    def __init__(self, **kw) -> None:
        
        super().__init__(**kw)
        
    def add(self, field: PeriodicField, x: np.ndarray, 
            weight: np.ndarray = None):
        
        raise NotImplementedError()
          
@numba.experimental.jitclass
class _PeriodicCIC:
    
    n_grids:    numba.int64
    l_box:      numba.float64
    l_grid:     numba.float64
    
    def __init__(self, n_grids: int, l_box: float) -> None:
        l_grid = l_box / n_grids
        
        self.n_grids = n_grids
        self.l_box = l_box
        self.l_grid = l_grid
    
    def window_at_dx(self, dx: float):
        w = 1.0 - np.abs(dx/self.l_grid)
        if w < 0.:
            w = 0.
        return w
    
    def window_at_ik(self, ik: np.ndarray):
        '''
        @ik: integer indices of the grid points in k-space, arbitrary shaped.
        '''
        sinc = np.sinc(ik / self.n_grids)
        w = sinc * sinc
        return w
    
    
          
class PeriodicCIC(MassAssigner):
    
    kind: str = 'cic'
    Impl = _PeriodicCIC
        
    def add(self, field: PeriodicField, x: np.ndarray, 
            weight: np.ndarray = None):
        
        ccfg, data = field.cell_cfg, field.data
        l_grid, n_grids = ccfg.l_grid, ccfg.n_grids
        
        assert x.ndim == 2
        n_pts = len(x)
        if weight is not None:
            assert weight.shape == (n_pts, )
        self.log(f'Add {n_pts} points to grids')
        
        x_rel = x / l_grid
        cid_l = np.floor(x_rel).astype(np.int64)
        w_lr = (cid_l + 1) - x_rel, x_rel - cid_l
        
        # periodic boundary condition
        cid_l[ cid_l < 0 ] += n_grids
        cid_l[ cid_l >= n_grids ] -= n_grids
        assert ((cid_l >= 0)&(cid_l < n_grids)).all()
        cid_r = cid_l + 1
        cid_r[cid_r == n_grids] = 0
        cid_lr = cid_l, cid_r
        
        for i0 in 0,1:
            for i1 in 0,1:
                for i2 in 0,1:
                    cid = cid_lr[i0][:,0], cid_lr[i1][:,1], cid_lr[i2][:,2]
                    w = w_lr[i0][:, 0] * w_lr[i1][:, 1] * w_lr[i2][:, 2]
                    if weight is not None:
                        w *= weight
                    NonPeriodicCIC._add_to(data, *cid, w)
                    

    def compensate_shape(self, field: PeriodicField):
        ccfg = field.cell_cfg
        n_grids, l_box = ccfg.n_grids, ccfg.l_box
        impl = _PeriodicCIC(n_grids, l_box)
        self.__div_shape_fn(field.data, impl)
        
    @staticmethod
    @numba.njit
    def __div_shape_fn(data: np.ndarray, impl: Impl):
        n = impl.n_grids
        n0, n1, n2 = data.shape
        nd2 = n//2
        nd2p1 = nd2 + 1
        assert n2 == nd2p1 or n2 == n
        for i0 in range(n0):
            ik0 = i0 - n if i0 >= nd2 else i0
            w0 = impl.window_at_ik(ik0)
            for i1 in range(n1): 
                ik1 = i1 - n if i1 >= nd2 else i1
                w1 = impl.window_at_ik(ik1)
                for i2 in range(n2):
                    ik2 = i2 - n if i2 >= nd2 else i2
                    w2 = impl.window_at_ik(ik2)
                    w =  w0*w1*w2                        
                    data[i0,i1,i2] *= 1.0 / w