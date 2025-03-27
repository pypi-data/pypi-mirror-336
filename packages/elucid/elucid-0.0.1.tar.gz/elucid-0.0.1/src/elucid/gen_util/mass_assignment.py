from __future__ import annotations
from .field import Field
from .mesh import Mesh
import numpy as np
from numba.experimental import jitclass
from numba import njit

class MassAssignment:
    
    def __init__(self, mesh: Mesh) -> None:
    
        self.mesh = mesh
        
    @staticmethod
    def from_method(self, method='CIC') -> MassAssignment:
        return {
            'CIC': CIC
        }[method]
        
    def compensate_shape(self, field: Field):
        raise NotImplementedError()

@jitclass
class _CIC_Auxiliary:
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def window_at_x(x: np.ndarray):
        '''
        @x: arbitrary shaped.
        '''
        w = 1.0 - np.abs(x)
        w = np.clip(w, 0.0, None)
        return w
    
    @staticmethod
    def window_at_ik(ik: np.ndarray, n_grids: int):
        '''
        @ik: integer indices of the grid points in k-space, arbitrary shaped.
        '''
        sinc = np.sinc(ik / n_grids)
        w = sinc * sinc
        return w
    
    @staticmethod
    def find_near(x: np.ndarray, n_grids: int):
        x_l = np.floor(x)
        w_l = 1.0 - (x - x_l)
        w_r = 1.0 - w_l
        
        ix_l = x_l.astype(np.int64)
        ix_r = ix_l + 1
        ix_r[ix_r == n_grids] = 0
        
        return (ix_l, ix_r), (w_l, w_r)
    
    @staticmethod
    def assign_point(field: np.ndarray, ix_lr, w_lr):
        for i0 in range(2):
            for i1 in range(2):
                for i2 in range(2):
                    field[..., ix_lr[i0][0], ix_lr[i1][1], ix_lr[i2][2] ] \
                        += w_lr[i0][0] * w_lr[i1][1] * w_lr[i2][2]
                        
    @staticmethod
    def assign_point_weighted(field: np.ndarray, ix_lr, w_lr, w):
        for i0 in range(2):
            for i1 in range(2):
                for i2 in range(2):
                    field[ix_lr[i0][0], ix_lr[i1][1], ix_lr[i2][2], ...] \
                        += w * w_lr[i0][0] * w_lr[i1][1] * w_lr[i2][2]
       
class CIC(MassAssignment):
       
    def to_field(self, xs: np.ndarray, field: Field, 
                 weights: np.ndarray = None):
        '''
        @xs: shaped (n_points, 3)
        @weights: None | array shaped (n_points, ) or (n_points, n_comps).
        @field: ScalarField or VectorField, shape = (n, n, n). 
        '''
        mesh = self.mesh
        n, h = mesh.n_grids, mesh.l_grid
        assert field.shape == (n, n, n)
        xs = xs / h
        xs[ xs < 0. ] += n
        xs[ xs >= n ] -= n
        assert np.all( (xs >= 0.) & (xs < n) )

        self.__assign_points(xs, weights, field.data, n)
        
    def compensate_shape(self, field: Field):
        mesh = self.mesh
        n = mesh.n_grids
        
        variant = field.fft_policy.variant
        if variant == 'real':
            assert field.shape == (n, n, n//2+1)
            is_real = True
        elif variant == 'complex':
            assert field.shape == (n, n, n)    
            is_real = False
        else:
            raise KeyError(f'Unknown variant: {variant}')    

        self.__div_shape_fn(field.data, n, is_real)
    
    @staticmethod
    @njit
    def __div_shape_fn(field: np.ndarray, n_grids: int, is_real: bool):
        aux = _CIC_Auxiliary()
        n_half = n_grids // 2
        n0, n1 = n_grids, n_grids
        n2 = n_half + 1 if is_real else n_grids
        for i0 in range(n0):
            ik0 = i0 - n_grids if i0 > n_half else i0
            for i1 in range(n1): 
                ik1 = i1 - n_grids if i1 > n_half else i1
                for i2 in range(n2):
                    ik2 = i2 - n_grids if i2 > n_half else i2
                    w = aux.window_at_ik(ik0, n_grids) * \
                        aux.window_at_ik(ik1, n_grids) * \
                        aux.window_at_ik(ik2, n_grids)
                    field[i0,i1,i2] *= 1.0 / w
                
    @staticmethod
    @njit
    def __assign_points(xs: np.ndarray, weights: np.ndarray, field: np.ndarray, 
                n_grids: int):
        aux = _CIC_Auxiliary()
        for i in range(xs.shape[0]):
            ix_lr, w_lr = aux.find_near(xs[i], n_grids)
            if weights is not None:
                aux.assign_point_weighted(field, ix_lr, w_lr, weights[i])
            else:
                aux.assign_point(field, ix_lr, w_lr)