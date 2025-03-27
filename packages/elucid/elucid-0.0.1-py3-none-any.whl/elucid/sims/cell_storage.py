from __future__ import annotations
from typing import Any, Dict, Tuple
import numpy as np
from pyhipp.core import abc, DataDict
from pyhipp.io import h5
import pandas as pd
from pyhipp_sims.sims import SnapshotLoaderDmo, SimInfo
from .sim_info_for_elucid import SimInfoForElucid
from functools import lru_cache, cached_property
from hilbertcurve.hilbertcurve import HilbertCurve
from ..gen_util.fields import CellConfig
    
class SnapshotStorage(abc.HasLog):
    def __init__(self, ld: SnapshotLoaderDmo, n_grids: int,
                 snap_dir: str,
                 **kw) -> None:
        
        super().__init__(**kw)
        
        sim_info_e = SimInfoForElucid(ld.sim_info)
        ccfg = CellConfig(n_grids, ld.sim_info.box_size)
        
        self.ld = ld
        self.sim_info_e = sim_info_e
        self.cell_config = ccfg
        self.snap_dir = snap_dir
        
    def snapshot_file(self, mode='r'):
        snap_dir = self.sim_info_e.snap_dir(self.ld.snap)
        fname = f'{snap_dir}/particles.hdf5'
        return h5.File(fname, mode)
        
    def create_snapshot_file(self):
        ccfg, ld = self.cell_config, self.ld
        tot_n_grids = ccfg.tot_n_grids
        cell_sizes = pd.Series(np.zeros(tot_n_grids, dtype=int))
        for (x,) in ld.iter_particles('dm', ('x', )):
            cid = ccfg.cid_3d_to_1d(ccfg.x_to_cid(x))
            sizes = pd.DataFrame({'cid': cid}).groupby('cid').size()
            cell_sizes.loc[sizes.index] += sizes.to_numpy()
        cell_sizes = cell_sizes.to_numpy()
        n_parts = cell_sizes.sum()
        
        snap = ld.snap
        m_particle = ld.sim_info.mass_table[1]
        with self.snapshot_file('w') as f:
            header = f.create_group('Header')
            header.attrs.dump({
                'snap': snap,
                'total_n_particles': n_parts,
                'n_cells': ccfg.tot_n_grids,
                'm_particle': m_particle,
            })
            header.datasets.dump({
                'cell_n_particles': cell_sizes,
            })
            grp_cells = f.create_group('Cells')
            for i, n in enumerate(cell_sizes):
                grp_cell = grp_cells.create_group(str(i))._raw
                grp_cell.create_dataset('x', shape=(n, 3), dtype=np.float32)
                grp_cell.create_dataset('v', shape=(n, 3), dtype=np.float32)
                grp_cell.create_dataset('id', shape=(n,), dtype=np.int64)
        
    def push_particles(self, buffer_size = 1 * 1024 * 1024 * 1024):
        buffer_n_p = int(buffer_size / 4 / (3+3+2))
        self.log(f'Will read chunks, each with {buffer_n_p} particles.')
        ccfg, ld = self.cell_config, self.ld  
        
        with self.snapshot_file('a') as f:
            hd = f['Header']
            n_cells = hd.attrs['n_cells']
            cell_sizes = hd.datasets['cell_n_particles']
            cell_offs = np.zeros(n_cells, dtype=int)
            grp_cells = f['Cells']
            grp_cells = [ grp_cells[str(i)] for i in range(n_cells) ]
            ld_iter = ld.iter_particles(
                'dm', ('x', 'v', 'id'), n_chunk=buffer_n_p)
            for x, v, id in ld_iter:
                cid = ccfg.cid_3d_to_1d(ccfg.x_to_cid(x))
                self.__write_chunk(grp_cells, cell_offs, 
                                   cid, x, v, id)
        assert (cell_offs == cell_sizes).all()
                
    @staticmethod            
    def __write_chunk(grp_cells: list[h5.Group], cell_offs: np.ndarray, 
        cid: np.ndarray, x: np.ndarray, v: np.ndarray, id: np.ndarray):
        
        dfs = pd.DataFrame({'cid': cid}).groupby('cid')
        for _cid, df in dfs:
            cell: h5.Group = grp_cells[_cid]
            b, n = cell_offs[_cid], len(df)
            e = b + n
            cell_offs[_cid] = e
            pids = df.index.to_numpy()
            cell['x']._raw[b:e] = x[pids]
            cell['v']._raw[b:e] = v[pids]
            cell['id']._raw[b:e] = id[pids]
        n_written = cell_offs.sum()
        print(f'particles {n_written=}')
        
class CellIter(abc.HasDictRepr, abc.HasLog):
    
    '''
    sim_info_m, snap, file, cell_cfg, cache_maxcell
    header/
        snap, total_n_particles, n_cells,       -- loaded from snapshot header
        sim_name, n_side, p, l_box              -- __add_header()
    '''
    
    # used in the impl of ngb iter
    ngb_off_1d = -1,0,1
    ngb_off_3d = np.array(np.meshgrid(ngb_off_1d, ngb_off_1d, ngb_off_1d, 
                                   indexing='ij')).reshape(3,-1).T
    
    #predefiend ld_spec for __call__().
    LoadSpec = Dict[str, Tuple[str]]
    ld_spec_x = {
        'ps': ('x', )
    }
    ld_spec_x_vol = {
        **ld_spec_x,
        'p_meta': ('volume', )
    }
    
    repr_attr_keys = ('header', 'domain_sample', 'cache_maxcell')

    def __init__(self, sim_info: SimInfo, 
                 snap: int, domain_sample = None,
                 cache_maxcell = None, **kw) -> None:
        
        super().__init__(**kw)
        
        sim_info_m = SimInfoForElucid(sim_info)
        file = h5.File(sim_info_m.root_file, 'r')
                
        self.sim_info_m = sim_info_m
        self.snap = snap
        self.cache_maxcell = cache_maxcell
        
        self.file = file
        self.domain_sample = domain_sample
        self.header = self.g_ps['Header'].attrs.load()
        self.__add_header()
        
    @cached_property
    def g_snap(self):
        return self.file[f'Snapshots/{self.snap}']
        
    @cached_property
    def g_ps(self):
        samp = self.domain_sample
        if samp is None:
            group = 'Particles'
        else:
            group = f'Domain/ParticleSamples/{samp}'
        return self.g_snap[group]
    
    @cached_property
    def g_p_meta(self):
        samp = self.domain_sample
        if samp is not None:
            raise KeyError(f'Do not have meta for sample {samp}')
        return self.g_snap['ParticleMeta']
        
    def __call__(self, ld_spec: LoadSpec, 
                 crange=None) -> Any:
        for cid_1d, cid_3d in self.iter_cell_id(crange):
            out = self.load_cell(ld_spec, cid_1d)
            out |= {
                'cid_1d': cid_1d,
                'cid_3d': cid_3d,
            }
            yield out
        
    def iter_x_with_ngbs(self, boundary_thick=10.0, crange=None):
        ld = lru_cache(maxsize=self.cache_maxcell,)(CellIter.load_ps)
        ccfg = self.cell_cfg
        l_box, l_grid = ccfg.l_box, ccfg.l_grid
        l_half, l_g_half = l_box * .5, l_grid * .5
        
        for cid, cid_3d, ngb_cids, _ in self.iter_cell_id_with_ngbs(crange):
            x_all = []
            mask_all = []
            x_anc = cid_3d * l_grid + l_g_half
            x_lb = x_anc - l_g_half - boundary_thick
            x_ub = x_anc + l_g_half + boundary_thick
            
            for ngb_cid in ngb_cids:
                x = ld(self, ngb_cid, ('x', ))['x'].copy()
                
                dtype = x.dtype
                dx = x - x_anc.astype(dtype)
                x[dx >= l_half] -= l_box
                x[dx < -l_half] += l_box
                
                sel = ((x >= x_lb) & (x < x_ub)).all(1)
                if cid == ngb_cid:
                    assert sel.all()
                x = x[sel]
                
                mask = np.zeros(len(x), dtype=bool)
                mask[...] = cid == ngb_cid
                
                x_all.append(x)
                mask_all.append(mask)
        
            yield cid, np.concatenate(x_all), np.concatenate(mask_all)
  
    
    def load_rect(self, x_range: np.ndarray, ld_spec: LoadSpec):
        '''
        @x_range: ndarray like [[x_min, x_max], [y_min, y_max], [z_min, z_max]].
                  Can be slightly overbound.
        Each returned particle property is concatenated by those from visited 
        cells. All the particles in `x_range` must be returned, possibly with 
        additional neighbor particles outside `x_range`.
        '''
        x_range = np.asarray(x_range)
        ccfg = self.cell_cfg
        cid_lb = ccfg.x_to_cid_no_shift(x_range[:, 0])
        cid_ub = ccfg.x_to_cid_no_shift(x_range[:, 1])
        _out = []
        cid_list = []
        for i0 in range(cid_lb[0], cid_ub[0]+1):
            for i1 in range(cid_lb[1], cid_ub[1]+1):
                for i2 in range(cid_lb[2], cid_ub[2]+1):
                    cid = np.array((i0, i1, i2))
                    ccfg.shift_cid_in(cid)
                    ccfg.test_bound_cid(cid)
                    cid_1d = ccfg.cid_3d_to_1d(cid)
                    _out.append(self.load_cell(ld_spec, cid_1d))
                    cid_list.append(cid)
        out = DataDict({
            k: DataDict({
                k1: None for k1 in v.keys()
            }) for k, v in _out[0].items()
        })
        for k, v in out.items():
            for k1 in tuple(v.keys()):
                v[k1] = np.concatenate([ d[k][k1] for d in _out ])
        out['cid_list'] = cid_list
        return out
  
    def load_cell(self, ld_spec: LoadSpec, cid_1d: int):
        loader_map = {
            'ps': self.load_ps,
            'p_meta': self.load_p_meta,
        }
        out = DataDict({
            ld_key: loader_map[ld_key](cell_id=cid_1d, keys=keys) 
                for ld_key, keys in ld_spec.items()
        })
        return out
  
  
    def load_ps(self, cell_id: int, keys: tuple[str]):
        return self.g_ps[f'Cells/{cell_id}'].datasets.load(keys=keys)
    
    def load_p_meta(self, cell_id: int, keys: tuple[str]):
        return self.g_p_meta[f'Cells/{cell_id}'].datasets.load(keys=keys)
  
    
    def iter_cell_id(self, crange=None):
        '''
        Produce an iterator of (cid_1d, cid_3d) with Peano-Hilbert order.
        '''
        n_dims = 3
        n_side, p = self.header['n_side', 'p']
        ccfg = self.cell_cfg
        idx_ub = np.array((n_side,)*n_dims)
        
        sf_curve = HilbertCurve(p, n_dims)
        
        for i in range(2**(p*n_dims)):
            cid_3d = np.array(sf_curve.point_from_distance(i))
            if (cid_3d >= idx_ub).any():
                continue
            cid_1d = ccfg.cid_3d_to_1d(cid_3d)
            if crange is not None:
                b, e = crange
                if cid_1d < b or cid_1d >= e:
                    continue
                
            yield cid_1d, cid_3d
            
    def iter_cell_id_with_ngbs(self, crange = None):
        ccfg = self.cell_cfg
        n_side = self.header['n_side']
        for cid_1d, cid_3d in self.iter_cell_id(crange):
            ngb_cid_3d = (cid_3d + self.ngb_off_3d + n_side) % n_side
            ngb_cid_1d = ccfg.cid_3d_to_1d(ngb_cid_3d)
            yield cid_1d, cid_3d, ngb_cid_1d, ngb_cid_3d
  
        
    def __add_header(self):
        n_cells = self.header['n_cells']
        n_side = 0
        while n_side**3 < n_cells:
            n_side += 1
        assert n_side**3 == n_cells
        
        p = 0
        while 2**p < n_side:
            p += 1
            
        self.log(f'Find space filling settings: {n_side=}, {p=}')
            
        info = self.sim_info_m.sim_info
        l_box, sim_name = info.box_size, info.name
        self.cell_cfg = CellConfig(n_side, l_box)
        self.header |= {
            'n_side': n_side,
            'p': p,
            'l_box': l_box,
            'sim_name': sim_name,
        }
        
    def to_simple_repr(self) -> dict:
        return {
            'type': type(self).__name__,
            'header': self.header,
            'cell_config': self.cell_cfg.to_simple_repr(),
        }
        
    def __enter__(self):
        return self
    
    def __exit__(self, *_):
        self.file.close()
        