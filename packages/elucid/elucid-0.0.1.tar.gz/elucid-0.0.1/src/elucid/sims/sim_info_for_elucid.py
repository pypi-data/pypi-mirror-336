from pyhipp_sims.sims import SimInfo

class SimInfoForElucid:
    def __init__(self, sim_info: SimInfo) -> None:
        self.sim_info = sim_info
        
    @property
    def root_dir(self):
        return self.sim_info.root_dir / 'elucid_workdir'
    
    @property
    def root_file(self):
        return self.root_dir / 'simulation.hdf5'
    
    
    def snap_dir(self, snap: int):
        return self.root_dir / 'snapshots' / str(snap)
    
    def snap_file(self, snap: int):
        return self.snap_dir(snap) / 'snapshot.hdf5'
    
    def particle_file(self, snap: int):
        return self.snap_dir(snap) / 'particles.hdf5'