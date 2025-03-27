from __future__ import annotations
from typing import Any
import numpy as np
from pyhipp.core import DataDict, abc
from pyhipp.io import h5
from ..sims import SimInfo, SimInfoForElucid, predefined
from .filter import Filter

class Catalog(abc.HasSimpleRepr, abc.HasLog):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def __len__(self):
        raise NotImplementedError()
    
    def __getitem__(self, key):
        raise NotImplementedError()

class HaloCatalog(abc.HasSimpleRepr):
    '''
    halos/
        id, x, v, m_mean200
    meta/
        n_halos,
        type, snap, z           -- Sim
    sim_info                    -- Sim
    r_halo(key)                 -- Sim
    '''
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        
        self.halos = DataDict()
        self.meta = DataDict()
    
    @classmethod
    def create(cls, **kw):
        raise NotImplementedError()
    
    def __len__(self):
        return len(self.meta['n_halos'])
    
    def __getitem__(self, key):
        return self.halos[key]
    
    def to_simple_repr(self) -> Any:
        out = self.meta.get_dict()
        out['halos.keys'] = tuple(self.halos.keys())
        return out
        
class SimHaloCatalog(HaloCatalog):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
    
        self.sim_info: SimInfo = None
    
    @classmethod
    def create(cls, src_info: SimInfo, snap: int, **load_kw):
        info_e = SimInfoForElucid(src_info)
        
        with h5.File(info_e.root_file) as f:
            g = f[f'Snapshots/{snap}/Groups/Halos']
            halos = g.datasets.load(**load_kw)
            meta = g.attrs.load()    
        if 'id' not in halos:
            halos['id'] = np.arange(meta['n_halos'])
        meta['type'] = cls.__name__
        meta['snap'] = snap
        meta['z'] = src_info.redshifts[snap]
        
        return cls.create_from_halos(halos, meta, src_info)
    
    @classmethod
    def create_from_halos(cls, halos: DataDict, meta: DataDict, 
                          sim_info: SimInfo):
        out = cls()
        out.halos |= halos
        out.meta |= meta
        out.sim_info = sim_info
        return out
    
    def r_halo(self, key='mean200'):
        assert key == 'mean200'
        o_key = 'r_mean200'
        
        halos = self.halos
        if o_key in halos:
            return halos[o_key]
        
        ht = self.sim_info.cosmology.halo_theory
        m_halo = self['m_mean200']
        z = self.meta['z']
        rho_halo = ht.rho_vir_mean(f=200.0, z=z)
        r_halo = ht.r_vir(m_halo, rho_halo).astype(m_halo.dtype)
        halos[o_key] = r_halo
        
        return r_halo
    
    def selected(self, spec: Any, filter='and'):
        assert filter == 'and'
        args = Filter.create_and(spec)(self)
        
        halos = { k: args(v) for k, v in self.halos.items()}
        
        meta = self.meta.copy()
        meta['n_halos'] = args.selected_size
        
        return self.create_from_halos(halos, meta, self.sim_info)