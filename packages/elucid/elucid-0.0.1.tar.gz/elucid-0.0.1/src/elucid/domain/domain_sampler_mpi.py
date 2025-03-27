from pyhipp.mpi import Comm, Pool, DistributedRng, Predefined as MpiPredef
from .domain_sampler import DomainSampler
from ..sims.cell_storage import CellConfig
from pathlib import Path
from pyhipp.core import abc, DataDict
import numpy as np
from pyhipp.io import h5
import pandas as pd

class DomainSamplerMpi(abc.HasDictRepr, abc.HasLog):
    '''
    @dump_to: each process must have a distinct path, e.g., 
                'particles.hdf5.{rank}'.
    '''
    attr_descrs = [
        ('hid', (), np.int64),
        ('x', (3,), np.float64),
        ('r_eff', (), np.float64)
    ]
    
    repr_attr_keys = ('pool', 'dom_samp', 'use_dist_rng', 'max_mass_per_task')
    
    def __init__(self, comm: Comm, dom_samp: DomainSampler, 
                 use_dist_rng = True, max_mass_per_task = 1.0e10,
                 **kw) -> None:
        
        super().__init__(**kw)
        
        pool = Pool(comm, gather_reply=False)
        
        rng = DistributedRng(pool.comm).get_sequential()
        dom_samp.set_rng(rng)
        
        self.pool = pool
        self.dom_samp = dom_samp
        self.use_dist_rng = use_dist_rng
        self.max_mass_per_task = max_mass_per_task
        
        self.sample = DataDict({k: [] for k, _, _ in self.attr_descrs})
        self.joined = False
        
    def run(self, report_interval = 1000) -> None:
        assert not self.joined
        pool, dom_samp, samp = self.pool, self.dom_samp, self.sample
        if pool.is_leader:
            self.log(f'Start sampling with {pool.n_workers} workers', 
                     timed=True)
            m_max = self.max_mass_per_task
            for hid in range(dom_samp.n_halos):
                m_halo = dom_samp.m_halo[hid]
                n_tasks = self.assign_task(hid, m_halo, m_max, pool)
                if n_tasks > 1:
                    self.log(f'Generate {n_tasks} tasks for {hid=}, {m_halo=}')
                if (hid + 1) % report_interval == 0:
                    self.log(f'Sampling for {hid+1}th halo ...', 
                             timed=True)
            pool.join()
            self.log(f'Joined workers', timed=True)
        else:
            for work in pool.works:
                hid, frac = work.content
                x, r_eff = dom_samp.sample(hid, sampling_fraction=frac)
                hid = np.full(len(x), hid)
                samp['hid'].append(hid)
                samp['x'].append(x)
                samp['r_eff'].append(r_eff)
        for k, shape, dt in self.attr_descrs:
            v = samp[k]
            if len(v) == 0:
                v = np.zeros((0,)+shape, dtype=dt)
            else:
                v = np.concatenate(v, axis=0, dtype=dt)
            samp[k] = v
        self.joined = True
        
    def dump(self, path: Path, cell_cfg: CellConfig):
        assert self.joined
        pool, dom_samp = self.pool, self.dom_samp
        cid, cell_sizes = self.__gather_sizes(cell_cfg)
        n_cells = len(cell_sizes)
        if pool.is_leader:
            self.log(f'Start dumping for {n_cells} cells ...')
            with h5.File(path, 'w') as f:
                header = f.create_group('Header')
                header.attrs.dump({
                    'snap': dom_samp.snap,
                    'total_n_particles': cell_sizes.sum(),
                    'n_cells': n_cells,
                    'm_particle': dom_samp.m_particle,
                })
                header.datasets.create('cell_n_particles', cell_sizes)
                self.log('Header created')
                
                grp_cells = f.create_group('Cells')
                for i, n in enumerate(cell_sizes):
                    grp_cell = grp_cells.create_group(str(i))._raw
                    for k, shape, dt in self.attr_descrs:
                        grp_cell.create_dataset(k, shape=(n,)+shape, dtype=dt)
                self.log('Cells created')
                        
            offs = np.zeros_like(cell_sizes)
            for w in pool.workers.values():
                self.log(f'Worker {w.pair_rank} dumping at offsets '
                         f'[{offs[0]} ... {offs[-1]}]')
                w.send(offs)
                offs = w.recv()
            assert np.all(offs == cell_sizes)
        else:
            leader = pool.leader
            offs = leader.recv()
            dfs = pd.DataFrame({'cid': cid}).groupby('cid')
            with h5.File(path, 'a') as f:
                grp_cells = f['Cells']
                for i, df in dfs:
                    grp_cell = grp_cells[str(i)]._raw
                    b = offs[i]; e = b + len(df)
                    idx = df.index.to_numpy()
                    for k, v in self.sample.items():
                        grp_cell[k][b:e] = v[idx]
                    offs[i] = e
            leader.send(offs)
    
    @staticmethod
    def assign_task(hid: int, m_halo: float, m_max: float, pool: Pool):
        frac, cum_frac, n_tasks = m_max / m_halo, 0., 0
        while True:
            n_tasks += 1
            _cum_frac = cum_frac + frac
            if _cum_frac > 1.0:
                pool.assign_work((hid, 1.0 - cum_frac))
                break
            pool.assign_work((hid, frac))
            cum_frac = _cum_frac
        return n_tasks
        
    def __gather_sizes(self, cell_cfg: CellConfig):
        samp, pool = self.sample, self.pool
        
        # shift x
        x = samp['x']
        for _ in range(5):
            if not cell_cfg.test_bound_x(x):
                cell_cfg.shift_x_in(x)
        assert cell_cfg.test_bound_x(x)
        
        # count cells        
        n_cells = cell_cfg.tot_n_grids
        cell_sizes = np.zeros(n_cells, dtype=np.int64)
        cid = cell_cfg.cid_3d_to_1d(cell_cfg.x_to_cid(x))
        _s = pd.DataFrame({'cid': cid}).groupby('cid').size()
        cell_sizes[_s.index.to_numpy()] = _s.to_numpy()
        
        # gather cell sizes
        buf = np.zeros_like(cell_sizes) if pool.is_leader else None
        pool.comm.Reduce(cell_sizes, buf, op=MpiPredef.sum, 
                         root=pool.leader_rank)

        return cid, (buf if pool.is_leader else cell_sizes)