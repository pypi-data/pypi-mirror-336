from __future__ import annotations
from numba.experimental import jitclass
from numba import float64, int64
import numpy as np
from ..gen_util import abc as abc_e

@jitclass
class _Cells:
    
    n_grids:    int64
    l_box:      float64
    l_half:     float64
    l_grid:     float64
    n_cells:    int64
    
    def __init__(self, n_grids: int, l_box: float) -> None:
        self.n_grids = n_grids
        self.l_box = l_box
        self.l_half = l_box * .5
        self.l_grid = l_box / n_grids
        self.n_cells = n_grids * n_grids * n_grids
    
    @staticmethod
    def create_single_cell(l_box: float) -> _Cells:
        return _Cells(1, l_box)
    
    def create_new_n_grids(self, n_grids: int) -> _Cells:
        return _Cells(n_grids, self.l_box)
    
    
    def x_to_cid_3d(self, x: np.ndarray):
        return np.floor(x / self.l_grid).astype(np.int64)
    
    def x_to_cid_1d(self, x: np.ndarray):
        return self.cid_3d_to_1d(self.x_to_cid_3d(x))
    
    def cid_3d_to_1d(self, cid_3d: np.ndarray):
        n_grids = self.n_grids
        i0, i1, i2 = (cid_3d + n_grids) % n_grids
        return (i0 * n_grids + i1) * n_grids + i2
    
    def cid_3d_to_1d_unsafe(self, cid_3d: np.ndarray):
        n_grids = self.n_grids
        i0, i1, i2 = cid_3d
        return (i0 * n_grids + i1) * n_grids + i2
    
    
    def shift_dx(self, dx: np.ndarray):
        '''
        dx is updated and returned.
        '''
        l_box, l_half = self.l_box, self.l_half
        for i in range(3):
            _dx = dx[i]
            if _dx >= l_half:
                _dx -= l_box
            elif _dx < -l_half:
                _dx += l_box
            dx[i] = _dx
        return dx
    
    def shift_x_in(self, x: np.ndarray):
        '''
        x is updated and returned.
        '''
        l_box = self.l_box
        for i in range(3):
            _x = x[i]
            if _x >= l_box:
                _x -= l_box
            elif _x < 0.:
                _x += l_box
            x[i] = _x
        return x
    
    def shift_x_to(self, x: np.ndarray, x0: np.ndarray):
        '''
        Return new (shifted) x.
        '''
        return x0 + self.shift_dx(x - x0)
    
    
    def is_bound_x(self, x: np.ndarray):
        return ((0.0 <= x) & (x < self.l_box)).all()
    
    def is_bound_cid_3d(self, cid_3d: np.ndarray):
        return ((0 <= cid_3d) & (cid_3d < self.n_grids)).all()
    
    def point_dist(self, x0: np.ndarray, x1: np.ndarray) -> float:
        '''
        Return squared distance in the periodic box.
        @x0, x1: (ndim, ) ndarrays.
        '''
        dx = self.shift_dx(x1 - x0) 
        return (dx*dx).sum()
    
    @staticmethod
    def point_dist_unsafe(x0: np.ndarray, x1: np.ndarray) -> float:
        dx = x1 - x0
        return (dx*dx).sum()
    
    def min_dist_to_cell(self, x: np.ndarray, x_cid_3d: np.ndarray, 
                         cid_3d: np.ndarray):
        '''
        Return squared distance.
        '''
        r_sq, l_half, l_grid, l_box = 0., self.l_half, self.l_grid, self.l_box
        for i in range(3):
            _x, x_cid, cid = x[i], x_cid_3d[i], cid_3d[i]
            if cid < x_cid:
                _x_cell = l_grid * (cid + 1)
            elif cid > x_cid:
                _x_cell = l_grid * cid
            else:
                _x_cell = _x
            dx = _x - _x_cell
            if dx >= l_half:
                dx -= l_box
            elif dx < -l_half:
                dx += l_box
            r_sq += dx * dx
        return r_sq

class Cells(abc_e.NumbaClassWrapper):
    
    Impl = _Cells
    impl_repr_items = ('n_grids', 'l_box', 'l_grid', 'n_cells')
    
@jitclass
class _CelledHalos:
    
    cells:          _Cells
    cell_sizes:     int64[:]
    cell_offs:      int64[:]
    
    n_halos:        int64
    sort_args:      int64[:]
    x:              float64[:,:]
    r:              float64[:]
    r_sq:           float64[:]
    cid_1d:         int64[:]
    r_max:          float64
    r_sq_max:       float64
    
    
    def __init__(self, cells: _Cells, x: np.ndarray = None, 
                 r: np.ndarray = None) -> None:
        
        self.cells = cells
        if x is not None:
            assert r is not None
            self.set_halos(x, r)
            
    def create_new_n_grids(self, n_grids: int) -> _CelledHalos:
        return _CelledHalos(self.cells.create_new_n_grids(n_grids), 
                            self.x, self.r)
        
    def set_halos(self, x: np.ndarray, r: np.ndarray) -> _CelledHalos:
        
        cells = self.cells
        n_halos = len(x)
        n_cells = cells.n_cells
        assert len(r) == n_halos
        
        # find cid
        cid_1d = np.empty(n_halos, dtype=np.int64)
        for i, _x in enumerate(x):
            _cid_3d = cells.x_to_cid_3d(_x)
            assert cells.is_bound_cid_3d(_cid_3d)
            cid_1d[i] = cells.cid_3d_to_1d_unsafe(_cid_3d)
        
        # count
        cell_sizes = np.zeros(n_cells, dtype=np.int64)
        for i in cid_1d:
            cell_sizes[i] += 1
        cell_offs = np.zeros(n_cells+1, dtype=np.int64)
        for i in range(n_cells):
            cell_offs[i+1] = cell_offs[i] + cell_sizes[i]
        
        # sort
        sort_args = np.argsort(cid_1d)
        x, r, cid_1d = x[sort_args], r[sort_args], cid_1d[sort_args]
        r_max = r.max()
        r_sq = r * r
        r_sq_max = r_max * r_max
        
        self.cell_sizes = cell_sizes
        self.cell_offs = cell_offs
        
        self.n_halos = n_halos
        self.sort_args = sort_args
        self.x = x
        self.r = r
        self.r_sq = r_sq
        self.cid_1d = cid_1d
        self.r_max = r_max
        self.r_sq_max = r_sq_max
                
        return self
    
    def min_dist_to(self, x: np.ndarray, cid_1d: int, 
                    hid: int, r_eff_sq: float):
        if self.cell_sizes[cid_1d] == 0:
            return hid, r_eff_sq
        
        offs = self.cell_offs
        b, e = offs[cid_1d], offs[cid_1d+1]
        
        x_hs, r_sq_hs = self.x, self.r_sq
        cells = self.cells
        x = cells.shift_x_to(x, x_hs[b])

        for i in range(b, e): 
            _r_eff_sq = cells.point_dist_unsafe(x, x_hs[i]) / r_sq_hs[i]
            if _r_eff_sq < r_eff_sq:
                hid, r_eff_sq = i, _r_eff_sq

        return hid, r_eff_sq
    
    def min_dist_to_expanded(self, policy: int, 
        x: np.ndarray, cid_3d: np.ndarray, hid: int, r_eff_sq: float):

        if policy == 0:
            return self.__expanded_only_adjacent(x, cid_3d, hid, r_eff_sq)

        return self.__expanded_with_diagonal(x, cid_3d, hid, r_eff_sq)
    
    def __expanded_only_adjacent(self, x: np.ndarray, cid_3d: np.ndarray, 
            hid: int, r_eff_sq: float):
        for dim in range(3):
            _cid_3d = cid_3d.copy()
            for off in (-1,1):
                _cid_3d[dim] = cid_3d[dim] + off
                cid_1d = self.cells.cid_3d_to_1d(_cid_3d)
                hid, r_eff_sq = self.min_dist_to(x, cid_1d, hid, r_eff_sq)
        return hid, r_eff_sq
    
    def __expanded_with_diagonal(self, x: np.ndarray, cid_3d: np.ndarray,
            hid: int, r_eff_sq: float):
        _cid_3d = cid_3d.copy()
        for off_0 in (-1,0,1):
            _cid_3d[0] = cid_3d[0] + off_0    
            for off_1 in (-1,0,1):
                _cid_3d[1] = cid_3d[1] + off_1
                for off_2 in (-1,0,1):
                    if off_0 == off_1 == off_2 == 0:
                        continue
                    _cid_3d[2] = cid_3d[2] + off_2
                    cid_1d = self.cells.cid_3d_to_1d(_cid_3d)
                    hid, r_eff_sq = self.min_dist_to(x, cid_1d, hid, r_eff_sq)
        return hid, r_eff_sq
    
    def min_dist_to_all(self, x: np.ndarray, 
                        hid: int, r_eff_sq: float):
        cells, x_hs, r_sq_hs = self.cells, self.x, self.r_sq
        for i in range(self.n_halos):
            _r_eff_sq = cells.point_dist(x, x_hs[i]) / r_sq_hs[i]
            if _r_eff_sq < r_eff_sq:
                hid, r_eff_sq = i, _r_eff_sq
        return hid, r_eff_sq
    
    
class CelledHalos(abc_e.NumbaClassWrapper):
    Impl = _CelledHalos
    impl_repr_items = ('n_halos', 'cell_sizes', 'r', ('cells', Cells))
    quantile_repr_items = ('cell_sizes', 'r')
    
    def __init__(self, impl: Impl, **kw) -> None:
        super().__init__(impl, **kw)
        self.impl: _CelledHalos
    
@jitclass
class _CelledMaxHaloRadii:
    
    cells:          _Cells
    max_r_sq:       float64[:]
    
    def __init__(self, celled_halos: _CelledHalos = None) -> None:
        
        self.cells = _Cells(1,  1.0)
        if celled_halos is not None:
            self.set_halos(celled_halos)
        
    def set_halos(self, celled_halos: _CelledHalos) -> _CelledMaxHaloRadii:
        
        cells = celled_halos.cells
        n_cells = cells.n_cells
        max_r_sq = np.zeros(n_cells, dtype=np.float64)
        
        r_sq = celled_halos.r_sq
        cell_offs = celled_halos.cell_offs
        for i in range(n_cells):
            b, e = cell_offs[i], cell_offs[i+1]
            if e - b > 0: max_r_sq[i] = r_sq[b:e].max()   
        
        self.cells = cells
        self.max_r_sq = max_r_sq
        
        return self
            
    def near(self, x: np.ndarray, r_max: float):
        cells = self.cells
        lbs, ubs = cells.x_to_cid_3d(x - r_max), \
            cells.x_to_cid_3d(x + r_max) + 1
        r_h_sq_max = 0.
        for i0 in range(lbs[0], ubs[0]):
            for i1 in range(lbs[1], ubs[1]):
                for i2 in range(lbs[2], ubs[2]):
                    cid_3d = np.array((i0,i1,i2), dtype=np.int64)
                    cid_1d = cells.cid_3d_to_1d(cid_3d)
                    _r_h_sq_max = self.max_r_sq[cid_1d]
                    if _r_h_sq_max > r_h_sq_max:
                        r_h_sq_max = _r_h_sq_max
        return r_h_sq_max
        
class CelledMaxHaloRadii(abc_e.NumbaClassWrapper):
    
    Impl = _CelledMaxHaloRadii
    impl_repr_items = ('max_r_sq', ('cells', Cells))
    quantile_repr_items = ('max_r_sq',)