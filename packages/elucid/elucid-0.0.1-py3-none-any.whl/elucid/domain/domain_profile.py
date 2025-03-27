from __future__ import annotations
from typing import Tuple, Iterable, Any
import numpy as np
from numba import int64, float64, njit
from numba.experimental import jitclass
import pandas as pd
from pyhipp.core import abc, dataproc as dp, DataDict
from pyhipp.io import h5
from pyhipp.astro.cosmology import model as cosm_model
from pyhipp.stats.binning import Bins, BinnedData
from .domain_locator import DomainLocator
from ..catalogs import SimHaloCatalog
from ..sims.cell_storage import CellIter
from pathlib import Path

class DomainProfile(abc.HasLog, abc.HasDictRepr):
    
    repr_attr_keys = ('halo_cat', 'cell_iter', 'm_key', 'lm_bins', 'r_bins', 
                      'cids_1d')
    
    def __init__(self, 
                 halo_cat: SimHaloCatalog, 
                 cell_iter: CellIter, 
                 lm_bins: Bins,
                 r_bins: Bins,
                 m_key = 'm_mean200',
                 dom_loc_init_pl: DomainLocator.Policy = None,
                 dom_loc_run_pl: DomainLocator.LocatePolicy = None,
                 **kw) -> None:
        super().__init__(**kw)

        dom_loc = DomainLocator(halo_cat, m_key=m_key, pl=dom_loc_init_pl)
        
        m_halo = halo_cat[m_key]
        lm = dp.Num.safe_lg(m_halo)
        r_data = [ BinnedData(r_bins, dtype=float, shape=(2,)) 
                   for _ in range(lm_bins.n_bins) ]
        
        self.halo_cat = halo_cat
        self.dom_loc = dom_loc
        self.dom_loc_run_pl = dom_loc_run_pl
        
        self.cell_iter = cell_iter
        
        self.m_key = m_key
        self.lm = lm
        self.lm_bins = lm_bins
        
        self.r_bins = r_bins
        self.r_data = r_data
        
        self.cids_1d = []
        
    def run(self, cids_1d: np.ndarray):
        cell_iter = self.cell_iter
        for cid_1d in cids_1d:
            self.log(f'Running on cell {cid_1d}', end=' ... ')
            data = cell_iter.load_cell(cell_iter.ld_spec_x_vol, cid_1d)
            self.__call_on_cell(*data['ps/x', 'p_meta/volume'])
        self.cids_1d.extend(cids_1d)
            
    def dump(self, group: h5.Group):
        self.log(f'Dumping meta', end=' ... ')
        sim_info = self.halo_cat.sim_info
        d = {
            'sim_name': sim_info.name,
            'm_key': self.m_key,
            'r_edges': self.r_bins.x_edges,
            'lm_edges': self.lm_bins.x_edges,
            'cids_1d': self.cids_1d,
            'm_particle': sim_info.mass_table[1],
            'lm_halos': self.lm,
        }
        group.datasets.dump(d)
        
        self.log(f'Dumping profiles', end=' ... ', named=False)
        g_profs = group.create_group('Profiles')
        for i, r_data in enumerate(self.r_data):
            n_particles, volumes = r_data.data.T
            d = {
                'n_particles': n_particles,
                'volumes': volumes,
            }
            g_profs.create_group(str(i)).datasets.dump(d)
        
        self.log('Done', named=False)
    
    @staticmethod
    def gather_dumps(groups: Iterable[h5.Group], to_group: h5.Group = None):
        for i_batch, group in enumerate(groups):
            g_profs = group['Profiles']
            if i_batch != 0:
                for i_m in range(m_n_bins):
                    d = g_profs[str(i_m)].datasets.load()
                    for k, v in d.items():
                        profs[i_m][k] += v
                continue    
            meta = group.datasets.load()
            meta.pop('cids_1d')
            m_n_bins = len(meta['lm_edges']) - 1
            assert m_n_bins == len(g_profs.keys())
            profs = [ g_profs[str(i_m)].datasets.load() 
                        for i_m in range(m_n_bins) ]
        
        m_p = meta['m_particle']
        for i in range(m_n_bins):
            n_p, vol = profs[i]['n_particles', 'volumes']
            rho = dp.Num.safe_div(n_p * m_p, vol)
            profs[i] |= {
                'rhos': rho,
            }
        if to_group is not None:
            to_group.datasets.dump(meta)
            g_profs = to_group.create_group('Profiles')
            for i, prof in enumerate(profs):
                g_profs.create_group(str(i)).datasets.dump(prof)
        
        meta |= {'profiles': profs}
        return meta

    def __call_on_cell(self, xs: np.ndarray, vols: np.ndarray):
        self.log(f'Locating domains for {len(xs)} particles', 
                 end=' ... ', named=False)
        hids, r_effs = self.dom_loc.locate(xs, pl=self.dom_loc_run_pl)
        
        sel = hids >= 0
        n_nosel = (~sel).sum()
        if self.verbose and n_nosel > 0:
            self.log(f'{n_nosel} particles not in halos')    
        r_effs, vols, lms = r_effs[sel], vols[sel], self.lm[hids[sel]]
        
        self.log(f'Adding to bins', end=' ... ', named=False)
        m_ids = self.lm_bins.locate(lms)
        df = pd.DataFrame({'m_id': m_ids, 'r_eff': r_effs, 'vol': vols})
        for m_id, grp in df.groupby('m_id'):
            if m_id < 0: continue
            r_effs, vols = grp['r_eff'].to_numpy(), grp['vol'].to_numpy()
            weights = np.stack([np.ones_like(r_effs), vols], axis=1)
            self.r_data[m_id].add(r_effs, weights)
        self.log('Done for the cell', named=False)
        

@jitclass
class _DomainProfileInterpolator:
    
    lms:    float64[:]
    rs:     float64[:]
    rhos:   float64[:,:]
    
    def __init__(self, lms: np.ndarray, rs: np.ndarray, 
                 rhos: np.ndarray) -> None:
        '''
        @lms: array, shape = (n_lm_bins,). 
        @rs:  array, shape = (n_r_bins,).
        @rhos: densities, shaped (n_lm_bins, n_r_bins). The returned from, e.g.,
               rho_of(), rho_profile_of(), are interpolated from rhos.
        '''
        self.lms = lms
        self.rs = rs
        self.rhos = rhos
        
    def rho_of(self, lm: float, r: float, lmid: int, rid: int) -> float:
        lms, rs, rhos = self.lms, self.rs, self.rhos
        lm_w_l, lm_w_r, lm_id_l, lm_id_r = self.find_weight(lms, lm, lmid)
        r_w_l, r_w_r, r_id_l, r_id_r = self.find_weight(rs, r, rid)
        rho_ll, rho_lr = rhos[lm_id_l, r_id_l], rhos[lm_id_l, r_id_r]
        rho_rl, rho_rr = rhos[lm_id_r, r_id_l], rhos[lm_id_r, r_id_r]
        return rho_ll * lm_w_l * r_w_l + \
            rho_lr * lm_w_l * r_w_r + \
            rho_rl * lm_w_r * r_w_l + \
            rho_rr * lm_w_r * r_w_r
            
    def rho_profile_of(self, lm: float, lmid: int) -> np.ndarray:
        lm_w_l, lm_w_r, lm_id_l, lm_id_r = self.find_weight(self.lms, lm, lmid)
        hist_l, hist_r = self.rhos[lm_id_l], self.rhos[lm_id_r]
        return lm_w_l * hist_l + lm_w_r * hist_r
        
    def find_weight(self, xs: float, x: float, xid: int):
        n_xs = len(xs)
        if xid == 0:
            w_l, w_r = 0., 1.
            xid_l, xid_r = 0, 0
        elif xid == n_xs:
            w_l, w_r = 1.0, 0.0
            xid_l, xid_r = n_xs-1, n_xs-1
        else:
            xid_l, xid_r = xid-1, xid
            x_l, x_r = xs[xid_l], xs[xid_r]
            dx = x_r - x_l
            w_l, w_r = (x_r - x) / dx, (x - x_l) / dx
        return w_l, w_r, xid_l, xid_r

class DomainProfileInterpolator(abc.HasDictRepr, abc.HasLog):
    
    Impl = _DomainProfileInterpolator
    
    repr_attr_keys = ('meta', 'impl')
    
    def __init__(self, profile_data: DataDict, **kw) -> None:
        
        super().__init__(**kw)
        
        rhos, m_key, m_halo_lb, z, \
        lm_edges, r_edges, cosm = profile_data[
            'profiles', 'm_key', 'm_halo_lb', 'z', 
            'lm_edges', 'r_edges', 'cosmology']
        m_key = m_key.decode()
        rho_mean = cosm_model.predefined[cosm.decode()].rho_matter(z)
        rhos /= rho_mean
        
        lms = .5 * (lm_edges[1:] + lm_edges[:-1])
        lms[-1] = lm_edges[-2]
        rs = .5 * (r_edges[1:] + r_edges[:-1])
        impl = _DomainProfileInterpolator(lms, rs, rhos)
        
        lm_range = lm_edges.min(), lm_edges.max()
        r_range = r_edges.min(), r_edges.max()
        
        vol_edges = 4. / 3. * np.pi * r_edges**3
        vol_bins = vol_edges[1:] - vol_edges[:-1]
        
        self.impl = impl
        self.r_edges, self.lm_edges = r_edges, lm_edges
        self.vol_edges = vol_edges
        self.vol_bins = vol_bins
        self.meta = DataDict({
            'm_key': m_key, 'm_halo_lb': m_halo_lb, 'z': z,
            'n_lm_bins': len(lms), 'n_r_bins': len(rs),
            'lm_range': lm_range, 'r_range': r_range,
            'rho_mean': rho_mean,
        })
        
    @staticmethod
    def from_file(file_name: Path, group_name: str):
        with h5.File(file_name) as f:
            g = f[group_name]
            profile_data = g.datasets.load()
        return DomainProfileInterpolator(profile_data)
    
    def rho_of(self, lm_halo: np.ndarray, r_eff: np.ndarray):
        '''
        Return density rho / rho_mean.
        '''
        
        lm_halo, r_eff = np.asarray(lm_halo), np.asarray(r_eff)
        assert lm_halo.ndim == 1
        assert lm_halo.shape == r_eff.shape
        
        impl = self.impl
        lmid = np.searchsorted(impl.lms, lm_halo)
        rid = np.searchsorted(impl.rs, r_eff)
        rho = self.__rho_of(impl, lm_halo, r_eff, lmid, rid)
        
        return rho
    
    def mass_profile_of(self, lm_halo: float):
        '''
        Return mass, dm / (rho_mean * R_halo^3), in each radial bin.
        '''
        impl = self.impl
        lmid = np.searchsorted(impl.lms, lm_halo)
        rhos = impl.rho_profile_of(lm_halo, lmid)
        masses = rhos * self.vol_bins
        return masses
        
    @staticmethod
    @njit
    def __rho_of(impl: _DomainProfileInterpolator, 
                 lm: np.ndarray, r: np.ndarray, 
                 lmid: np.ndarray, rid: np.ndarray):
        out = np.empty_like(lm)
        for i in range(len(lm)):
            out[i] = impl.rho_of(lm[i], r[i], lmid[i], rid[i])
        return out

    