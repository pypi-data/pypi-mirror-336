from __future__ import annotations
from numba.experimental import jitclass
from numba import float64, int64, bool_, njit, prange
import numba
import numpy as np
from ..gen_util import abc as abc_e
from pyhipp.core import abc
from .cell import _CelledHalos, _CelledMaxHaloRadii, _Cells, CelledHalos, Cells, CelledMaxHaloRadii
from dataclasses import dataclass
from ..catalogs import SimHaloCatalog


@jitclass
class _DomainLocatorDetail:
    src_celled_halos:                   _CelledHalos
    celled_halos:                       _CelledHalos
    big_halos:                          _CelledHalos
    hid_map:                            int64[:]        # hid -> offset in src_celled_halos (x, r, etc.)
    
    brute_force:                        bool_
    
    pre_chk_r_eff_max:                  float64
    pre_chk_n_big_halos:                int64
    pre_chk_expand:                     bool_
    pre_chk_expand_policy:              int64
    pre_chk_expand_r_eff_min:           float64
    pre_chk_expand_r_min:               float64
    
    r_max:                              float64
    celled_r_h_max:                     _CelledMaxHaloRadii
    use_celled_r_h_max:                 bool_
    celled_r_h_max_n_grids:             int64
    sort_ngb_cells:                     bool_
    exclude_cell_by_dist:               bool_

    def __init__(self, 
        celled_halos:                   _CelledHalos,
        brute_force:                    bool,
        pre_chk_r_eff_max:              float, 
        pre_chk_n_big_halos:            int,
        pre_chk_expand:                 bool,
        pre_chk_expand_policy:          int,            # 0: adjacent, 1: adjacent + diagonal
        pre_chk_expand_r_eff_min:       float,
        pre_chk_expand_r_min:           float,
        r_max:                          float,
        use_celled_r_h_max:             bool,
        celled_r_h_max_n_grids:         int,
        sort_ngb_cells:                 bool,
        exclude_cell_by_dist:           bool,
    ) -> None:

        # split halos into big (pre-chcked) and small
        cells, n_halos =  celled_halos.cells, celled_halos.n_halos
        src_celled_halos = celled_halos
        assert n_halos >= 1 
        assert pre_chk_expand_policy in (0,1)
        
        pre_chk_n_big_halos = min(pre_chk_n_big_halos, n_halos-1)
        if pre_chk_n_big_halos > 0:
            x, r = celled_halos.x, celled_halos.r
            args = np.argsort(r)
            
            n_small_halos = n_halos - pre_chk_n_big_halos
            args_small = args[:n_small_halos]
            args_big = args[n_small_halos:]
            
            celled_halos = _CelledHalos(cells, x[args_small], r[args_small])
            big_halos = _CelledHalos(
                _Cells(1, cells.l_box), x[args_big], r[args_big])
            hid_map = np.concatenate((
                args_small[celled_halos.sort_args],
                args_big[big_halos.sort_args]
            ))
        else:
            big_halos = _CelledHalos(_Cells(1, cells.l_box), None, None)
            hid_map = np.arange(n_halos, dtype=np.int64)
            
        self.src_celled_halos = src_celled_halos
        self.celled_halos = celled_halos 
        self.big_halos = big_halos
        self.hid_map = hid_map
        
        self.brute_force = brute_force
        
        self.pre_chk_r_eff_max = pre_chk_r_eff_max
        self.pre_chk_n_big_halos = pre_chk_n_big_halos
        self.pre_chk_expand = pre_chk_expand
        self.pre_chk_expand_policy = pre_chk_expand_policy
        self.pre_chk_expand_r_eff_min = pre_chk_expand_r_eff_min
        self.pre_chk_expand_r_min = pre_chk_expand_r_min
        
        # create look-up cells for max halo radius
        if not use_celled_r_h_max:
            ch = None
        else:
            assert celled_r_h_max_n_grids > 0
            ch = celled_halos.create_new_n_grids(celled_r_h_max_n_grids)
        celled_r_h_max = _CelledMaxHaloRadii(ch)
        
        self.r_max = r_max
        self.celled_r_h_max = celled_r_h_max
        self.use_celled_r_h_max = use_celled_r_h_max
        self.celled_r_h_max_n_grids = celled_r_h_max_n_grids
        self.sort_ngb_cells = sort_ngb_cells
        self.exclude_cell_by_dist = exclude_cell_by_dist
        
    def locate(self, x: np.ndarray):
        '''
        Return: 
        - Index into cell_halos (x, r, etc) passed to __init__().
        - r_eff to the closest halo.
        '''
        x = x.astype(np.float64)
        if self.brute_force:
            hid, r_eff_sq = self.brute_force_chk(x)
        else:
            cid_3d, hid, r_eff_sq, expanded = self.pre_chk(x)
            hid, r_eff_sq = self.post_chk(x, cid_3d, hid, r_eff_sq, expanded)
            if hid >= 0:
                hid = self.hid_map[hid]
        r_eff = np.sqrt(r_eff_sq)
        return  hid, r_eff
        
    def brute_force_chk(self, x: np.ndarray):
        ch = self.src_celled_halos
        n_halos, cells, xs, r_sq_hs = ch.n_halos, ch.cells, ch.x, ch.r_sq
        hid, r_eff_sq = -1, self.pre_chk_r_eff_max**2
        for i in range(n_halos):
            _r_eff_sq = cells.point_dist(x, xs[i]) / r_sq_hs[i]
            if _r_eff_sq < r_eff_sq:
                hid = i
                r_eff_sq = _r_eff_sq
        return hid, r_eff_sq
        
    def pre_chk(self, x: np.ndarray):
        c_halos = self.celled_halos
        
        cells = c_halos.cells
        cid_3d = cells.x_to_cid_3d(x)
        cid_1d = cells.cid_3d_to_1d(cid_3d)

        hid, r_eff_sq = -1, self.pre_chk_r_eff_max**2
        hid, r_eff_sq = c_halos.min_dist_to(x, cid_1d, hid, r_eff_sq)
        
        # check for big halos one by one
        if self.pre_chk_n_big_halos > 0:
            _hid, r_eff_sq = self.big_halos.min_dist_to_all(x, hid, r_eff_sq)
            if _hid != hid:
                hid = _hid + c_halos.n_halos
                
        # expand search radius for small halos
        expanded = False
        if self.pre_chk_expand:
            r_sq = self.__r_sq_from_eff(hid, r_eff_sq) if hid >= 0 \
                else self.r_max**2
            if r_sq >= self.pre_chk_expand_r_min**2 \
                or r_eff_sq >= self.pre_chk_expand_r_eff_min**2:
                hid, r_eff_sq = c_halos.min_dist_to_expanded(
                    self.pre_chk_expand_policy, x, cid_3d, hid, r_eff_sq)
                expanded = True
        
        return cid_3d, hid, r_eff_sq, expanded
    
    def post_chk(self, x: np.ndarray, cid_3d: np.ndarray,
        hid: int, r_eff_sq: float, expanded: bool):

        r_sq_max, c_halos, c_r_h_max = (self.r_max**2, 
            self.celled_halos, self.celled_r_h_max)
        r_h_sq_max = c_halos.r_sq_max
        r_sq_max = min(r_eff_sq * r_h_sq_max, r_sq_max)
        r_max = np.sqrt(r_sq_max)
        
        # try to shrink r_max use celled_r_h_max
        if self.use_celled_r_h_max:
            r_h_sq_max = c_r_h_max.near(x, r_max)
            r_sq_max = min(r_eff_sq * r_h_sq_max, r_sq_max)
            r_max = np.sqrt(r_sq_max)
            
        cells = c_halos.cells
        lbs, ubs = cells.x_to_cid_3d(x - r_max), \
            cells.x_to_cid_3d(x + r_max) + 1
        
        if not self.sort_ngb_cells:
            for i0 in range(lbs[0], ubs[0]): 
                for i1 in range(lbs[1], ubs[1]):
                    for i2 in range(lbs[2], ubs[2]):
                        ngb_cid_3d = np.array((i0,i1,i2), dtype=np.int64)
                        ngb_cid_1d = cells.cid_3d_to_1d(ngb_cid_3d)
                        if not self.__cell_needs_chk(x, ngb_cid_3d, ngb_cid_1d, 
                            cid_3d, expanded, r_sq_max): continue
                        hid, r_eff_sq = c_halos.min_dist_to(x, ngb_cid_1d, 
                            hid, r_eff_sq)
                        r_sq_max = min(r_eff_sq * r_h_sq_max, r_sq_max) 
            return hid, r_eff_sq
        
        for i0 in self.__sort_cids(cid_3d[0], lbs[0], ubs[0]):
            for i1 in self.__sort_cids(cid_3d[1], lbs[1], ubs[1]):
                for i2 in self.__sort_cids(cid_3d[2], lbs[2], ubs[2]):
                    ngb_cid_3d = np.array((i0,i1,i2), dtype=np.int64)
                    ngb_cid_1d = cells.cid_3d_to_1d(ngb_cid_3d)
                    if not self.__cell_needs_chk(x, ngb_cid_3d, ngb_cid_1d, 
                        cid_3d, expanded, r_sq_max): continue
                    hid, r_eff_sq = c_halos.min_dist_to(x, ngb_cid_1d, 
                        hid, r_eff_sq)
                    r_sq_max = min(r_eff_sq * r_h_sq_max, r_sq_max) 
                    
        return hid, r_eff_sq
        
    def __r_sq_from_eff(self, hid, r_eff_sq):
        c_halos = self.celled_halos
        if hid >= c_halos.n_halos:
            r_sq = r_eff_sq * self.big_halos.r_sq[hid-c_halos.n_halos]
        else:
            r_sq = r_eff_sq * c_halos.r_sq[hid]
        return r_sq        
              
    def __cell_needs_chk(self, x: np.ndarray, 
        cid_3d: np.ndarray, cid_1d: int, x_cid_3d: np.ndarray, 
        expanded: bool, r_sq_max: float):
        
        c_halos = self.celled_halos
        if c_halos.cell_sizes[cid_1d] == 0:
            return False
        
        # try to exclude cells that had been visited in pre_chk().
        d_cid = cid_3d - x_cid_3d
        if self.pre_chk_expand and expanded:
            if self.pre_chk_expand_policy == 0:
                if np.abs(d_cid).sum() <= 1: 
                    return False
            elif (np.abs(d_cid) <= 1).all():
                    return False
        elif not d_cid.any():
            return False
        
        # try to exclude distant cells
        if self.exclude_cell_by_dist:
            r_sq = c_halos.cells.min_dist_to_cell(x, x_cid_3d, cid_3d)
            if r_sq >= r_sq_max:
                return False
            
        return True
    
    def __sort_cids(self, cid: int, lb: int, ub: int):
        out_cids = np.arange(lb, ub)
        d_cids = np.abs(out_cids - cid)
        args = np.argsort(d_cids)
        return out_cids[args]


class DomainLocatorDetail(abc_e.NumbaClassWrapper):
    Impl = _DomainLocatorDetail
    impl_repr_items = (
        ('src_celled_halos', CelledHalos),
        ('celled_halos', CelledHalos), 
        ('big_halos', CelledHalos),
        'brute_force',
        'pre_chk_r_eff_max', 
        'pre_chk_n_big_halos', 
        'pre_chk_expand', 
        'pre_chk_expand_policy',
        'pre_chk_expand_r_eff_min', 
        'pre_chk_expand_r_min',
        'r_max', 
        ('celled_r_h_max', CelledMaxHaloRadii),
        'use_celled_r_h_max', 
        'celled_r_h_max_n_grids',
        'sort_ngb_cells', 
        'exclude_cell_by_dist',
    )


@dataclass
class Policy:
    n_grids:                        int     = 16
    brute_force:                    bool    = False
    pre_chk_r_eff_max:              float   = 100.0
    pre_chk_n_big_halos:            int     = 16
    pre_chk_expand:                 bool    = True    
    pre_chk_expand_policy:          int     = 0
    pre_chk_expand_r_eff_min:       float   = 10.0
    pre_chk_expand_r_min:           float   = 10.0
    r_max:                          float   = 100.0
    use_celled_r_h_max:             bool    = True
    celled_r_h_max_n_grids:         int     = 8
    sort_ngb_cells:                 bool    = False
    exclude_cell_by_dist:           bool    = True

    def create_detail(self, celled_halos: CelledHalos):
        
        ch: _CelledHalos = celled_halos.impl
        assert ch.cells.n_grids == self.n_grids
        detail = DomainLocatorDetail.create(
            celled_halos            = ch,
            **self.__detail_kw
        )
        return detail
    
    @property
    def __detail_kw(self) -> dict:
        keys = (
            'brute_force', 
            'pre_chk_r_eff_max', 'pre_chk_n_big_halos', 'pre_chk_expand', 
            'pre_chk_expand_policy', 'pre_chk_expand_r_eff_min', 
            'pre_chk_expand_r_min', 'r_max', 'use_celled_r_h_max',
            'celled_r_h_max_n_grids', 'sort_ngb_cells',
            'exclude_cell_by_dist',)
        return { k: getattr(self, k) for k in keys }


@dataclass
class LocatePolicy:
    pass

class DomainLocator(abc.HasLog, abc.HasSimpleRepr):
    
    Detail          = DomainLocatorDetail
    Policy          = Policy
    LocatePolicy    = LocatePolicy
    
    def __init__(self, halo_cat: SimHaloCatalog, 
                 m_key = 'm_mean200', pl = None, **kw) -> None:
        '''
        @halo_cat: 'x', m_key, and r_halo() are used. 'x' is shifted into the 
        box before constructing the locator.
        '''
        
        super().__init__(**kw)
    
        if pl is None:
            pl = Policy()
            
        celled_halos = self.__take_halos(halo_cat, m_key, pl)
        detail = pl.create_detail(celled_halos)
        
        self.m_key, self.pl  = m_key, pl
        self.celled_halos = celled_halos
        self.detail = detail
    
    def to_simple_repr(self) -> dict:
        return {
            'm_key':    self.m_key,
            'pl':       self.pl,
            'detail':   self.detail.to_simple_repr(),
        }
        
    def locate(self, x: np.ndarray, pl: LocatePolicy = None):
        '''
        @x: np.ndarray, shape=(n_points, 3).
            Each of x can be slightly outside the box for which a periodic 
            boundary condition is adopted.
        Return:
        - hids: indices into matched halos in halo_cat of __init__(). 
          -1 for no matching.
        - r_effs: effective distances to the matched halos.
        '''
        
        if pl is None:
            pl = LocatePolicy()
        
        detail, sort_args = self.detail.impl, self.celled_halos.impl.sort_args
        out = self.__locate(x, detail, sort_args)        
        return out
        
    @staticmethod
    def __take_halos(halo_cat: SimHaloCatalog, m_key: str, pl: Policy):
        assert m_key == 'm_mean200'
        
        sim_info = halo_cat.sim_info
        dt = np.float64
        x = halo_cat['x'].astype(dt)
        r = halo_cat.r_halo('mean200').astype(dt)
        
        cells = Cells.create(n_grids=pl.n_grids, l_box=sim_info.box_size)
        DomainLocator.__shift_xs_in(x, cells.impl)
        out = CelledHalos.create(cells=cells, x=x, r=r)
        return out
            
    @staticmethod
    @njit
    def __shift_xs_in(xs: np.ndarray, cells: _Cells):
        n_points = len(xs)
        for i in range(n_points):
            cells.shift_x_in(xs[i])
    
    @staticmethod
    @njit
    def __locate(xs: np.ndarray, detail: _DomainLocatorDetail, 
                 sort_args: np.ndarray):
        n_points = len(xs)
        hids = np.empty(n_points, dtype=np.int64)
        r_effs = np.empty(n_points, dtype=np.float64)
        for i, _x in enumerate(xs):
            hid, r_eff = detail.locate(_x)
            if hid >= 0:
                hid = sort_args[hid]
            hids[i] = hid
            r_effs[i] = r_eff
        return hids, r_effs
    
    @staticmethod
    @njit(parallel=True)
    def __locate_parallel(xs: np.ndarray, detail: _DomainLocatorDetail):
        n_points = len(xs)
        hids = np.empty(n_points, dtype=np.int64)
        r_effs = np.empty(n_points, dtype=np.float64)
        for i in prange(n_points):
            _x = xs[i]
            hid, r_eff = detail.locate(_x)
            hids[i] = hid
            r_effs[i] = r_eff
        return hids, r_effs