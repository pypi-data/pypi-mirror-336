from __future__ import annotations
from pyhipp.core import abc
from typing import Tuple, Union
import numpy as np
from numba import njit

class NonPeriodicField(abc.HasDictRepr):
    
    Shape = Tuple[int, ...]
    Axes = Tuple[int, ...]
    DType = np.dtype
    
    def __init__(self, data: np.ndarray, 
                 spatial_n_dims: int = 3, **kw) -> None:
        
        super().__init__(**kw)
        
        self.data = data
        self.spatial_n_dims = spatial_n_dims
        
    @classmethod
    def from_shape(cls, shape: Shape, dtype: DType = np.float64, 
                   fill = 0, **init_kw):
        if fill is not None:
            if fill == 0:
                data = np.zeros(shape, dtype=dtype)
            else:
                data = np.full(shape, fill, dtype=dtype)
        else:
            data = np.empty(shape, dtype=dtype)
        return cls(data=data, **init_kw)
            
    @property
    def dtype(self) -> np.dtype:
        return self.data.dtype
    
    @property
    def n_dims(self) -> int:
        return self.data.ndim
    
    @property
    def shape(self) -> Shape:
        return self.data.shape
    
    @property
    def elem_shape(self) -> Shape:
        return self.shape[self.spatial_n_dims:]
    
    @property
    def spatial_axes(self) -> Axes:
        return tuple(dim for dim in range(self.spatial_n_dims))
    
    def to_simple_repr(self) -> dict:
        out = super().to_simple_repr()
        out |= {
            'shape': self.shape,
            'dtype': self.dtype,
            'spatial_n_dims': self.spatial_n_dims
        }
        return out
    
class NonPeriodicCIC(abc.HasDictRepr, abc.HasLog):
    
    repr_attr_keys = ('x_range', 'n_grids', 'l_grid', 'field')
    
    Field = NonPeriodicField
    
    def __init__(self, 
                 x_range: np.ndarray, 
                 n_grids: Union[np.ndarray, int] = 10,
                 dtype = np.float64,
                 field: Field = None,
                 **kw) -> None:
        '''
        @x_range: ndarray of shape (3, 2), specifying the lower and upper bounds
                  of three dimensions, or of shape (2,), the bounds of every 
                  dimension.
        @n_grids: the numbers of grid points of three dimensions. In each 
                  dimension, the first and last grid points are at the lower 
                  and upper bounds, respectively.
        '''
        super().__init__(**kw)
        
        if np.isscalar(n_grids):
            n_grids = n_grids, n_grids, n_grids
        n_grids = np.array(n_grids, dtype=int)
        assert n_grids.shape == (3,)
        n_cells = n_grids - 1
        
        x_range = np.array(x_range, dtype=float)
        if x_range.ndim == 1:
            x_range = np.array([x_range, x_range, x_range])
        assert x_range.shape == (3, 2)
        
        self.log(f'Field data shape = {n_grids}')
        if field is None:
            field = NonPeriodicCIC.Field.from_shape(
                n_grids, dtype=dtype)
        assert field.shape == tuple(n_grids)
        
        x_lb, x_ub = x_range.T
        l_grid = (x_ub - x_lb) / n_cells
        
        self.x_range = x_range
        self.n_cells = n_cells
        self.n_grids = n_grids
        self.x_lb, self.x_ub, self.l_grid = x_lb, x_ub, l_grid
        self.field = field
        
    def add(self, x: np.ndarray, weight: np.ndarray = None):
        field = self.field
        
        assert x.ndim == 2
        n_pts = len(x)
        if weight is not None:
            assert weight.shape == (n_pts, )
            
        x = x - self.x_lb
        cid_l = np.floor(x / self.l_grid).astype(np.int64)
        sel = ((cid_l >= 0) & (cid_l < self.n_cells)).all(1)
        cid_l, x = cid_l[sel], x[sel]
        if weight is not None:
            weight = weight[sel]
        n_pts_sel = len(x)
        self.log(f'Add {n_pts_sel}/{n_pts} points to grids')
        
        cid_r = cid_l + 1
        cid_lr = cid_l, cid_r
        x_rel = x / self.l_grid
        w_lr = cid_r - x_rel, x_rel - cid_l
        
        for i0 in 0,1:
            for i1 in 0,1:
                for i2 in 0,1:
                    cid = cid_lr[i0][:,0], cid_lr[i1][:,1], cid_lr[i2][:,2]
                    w = w_lr[i0][:, 0] * w_lr[i1][:, 1] * w_lr[i2][:, 2]
                    if weight is not None:
                        w *= weight
                    self.__add_to(field.data, *cid, w)
    
    @staticmethod
    @njit
    def _add_to(field: np.ndarray, cid0: np.ndarray, 
                 cid1: np.ndarray, cid2: np.ndarray, w: np.ndarray):
        _, n1, n2 = field.shape
        field = field.ravel()
        for i in range(len(w)):
            _cid0, _cid1, _cid2, _w = cid0[i], cid1[i], cid2[i], w[i]
            off = (_cid0 * n1 + _cid1) * n2 + _cid2
            field[off] += _w