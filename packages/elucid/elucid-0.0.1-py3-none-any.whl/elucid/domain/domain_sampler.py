from pyhipp.core import abc, DataDict
from pyhipp.stats.random import Rng
import numpy as np
from scipy.stats import rv_histogram
from ..catalogs import SimHaloCatalog
from .domain_profile import DomainProfileInterpolator
from .domain_locator import DomainLocator

class DomainSampler(abc.HasLog, abc.HasDictRepr):
    
    repr_attr_keys = ('n_halos', 'profile', 'm_particle', 
                      'nbins_r1', 'nbins_max')
    def __init__(self, 
        halo_cat:        SimHaloCatalog, 
        profile:         DomainProfileInterpolator, 
        m_particle:      float                      = None,
        r_eff_max:       float                      = 30.0,
        dom_loc_init_pl: DomainLocator.Policy       = None, 
        dom_loc_run_pl:  DomainLocator.LocatePolicy = None,
        seed                                        = 0, 
        **kw) -> None:
        
        super().__init__(**kw)
        
        m_key = profile.meta['m_key']
        m_halo: np.ndarray = halo_cat[m_key]
        x_halo: np.ndarray = halo_cat['x']
        assert m_key == 'm_mean200'
        r_halo: np.ndarray = halo_cat.r_halo('mean200')
        dom_loc = DomainLocator(halo_cat, m_key=m_key, pl=dom_loc_init_pl)
        
        n_bins_r1, n_bins_max = np.searchsorted(profile.r_edges, 
            [1.0001, r_eff_max+1.0e-4]) - 1
        r_edges = profile.r_edges[:n_bins_max+1]
        rng = Rng(seed)
        snap = halo_cat.meta['snap']
        if m_particle is None:
            info = halo_cat.sim_info
            m_particle = info.mass_table[info.part_type_index.dm]
        
        self.snap = snap
        self.m_halo, self.x_halo, self.r_halo = m_halo, x_halo, r_halo
        self.n_halos = len(m_halo)
        self.dom_loc = dom_loc
        self.dom_loc_run_pl = dom_loc_run_pl
        
        self.profile = profile
        self.m_particle = m_particle
        self.nbins_r1, self.nbins_max = n_bins_r1, n_bins_max
        self.r_edges = r_edges                          # bin edges of r_eff
        self.rng = rng
        
        self.log(f'Initialized. snap = {self.snap}, {m_particle=}, '
            f'r_eff bin edges = '
            f'[{r_edges[0]} ... {r_edges[n_bins_r1]} ... {r_edges[-1]}]')
        
    def set_rng(self, rng: Rng) -> None:
        self.rng = rng
        
    def sample(self, hid: int, sampling_fraction: float = 1.0):
        assert hid >= 0 and hid < len(self.m_halo)
        x_halo, m_halo, r_halo = self.x_halo[hid], \
            self.m_halo[hid], self.r_halo[hid]
        return self.sample_at(x_halo, m_halo, r_halo, 
            accept_in_domain=hid, sampling_fraction=sampling_fraction)
        
    def sample_at(self, x_halo: np.ndarray, m_halo: float, r_halo: float,
            accept_in_domain: int = None, sampling_fraction: float = 1.0):
        '''
        Give the sampled particles near one halo at `x` with mass `m_halo`.
        '''
        n_r1, n_max = self.nbins_r1, self.nbins_max
        r_edges, profile, rng = self.r_edges, self.profile, self.rng
        m_p = self.m_particle
        dom_loc, pl = self.dom_loc, self.dom_loc_run_pl
        
        masses = profile.mass_profile_of(np.log10(m_halo))[:n_max]
        m_total = masses.sum() / masses[:n_r1].sum() * m_halo
        m_sampled = m_total * sampling_fraction
        n_ps =  int(np.floor(m_sampled / m_p))
        rv, prob = rng.random(), (m_sampled - n_ps * m_p) / m_p
        if rv < prob:
            n_ps += 1
        if self.verbose:
            self.log(f'Sampling for {m_halo=}. {m_total=}, '
                     f'{sampling_fraction=}, {m_sampled=}, {n_ps=}.')

        r_effs = rv_histogram((masses, r_edges), 
            density=False, seed=rng._np_rng).rvs(size=n_ps)
        x_ps = rng.uniform_sphere(size=n_ps) * (r_effs*r_halo)[:, None] + x_halo
        if accept_in_domain is None:
            return x_ps, None
        
        n_sampled = len(x_ps)
        hids, r_effs = dom_loc.locate(x_ps, pl=pl)
        sel = hids == accept_in_domain
        x_ps, r_effs = x_ps[sel], r_effs[sel]
        n_accepted = len(x_ps)
        if self.verbose:
            self.log(f'Accepted {n_accepted} / {n_sampled} particles')
        return x_ps, r_effs

        
