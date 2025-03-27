from scipy.spatial import Delaunay
from pyhipp.core import abc
from functools import cached_property
from numba import njit
import numpy as np
from pyhipp.io import h5
from .cell_storage import CellIter

class Triangulation(abc.HasLog):
    def __init__(self, points: np.ndarray, **kw) -> None:
        super().__init__()
        
        tri = Delaunay(points)
        assert len(tri.coplanar) == 0
        points = tri.points
        n_dims = points.shape[1]
        n_points = len(points)
        
        self.tri = tri
        self.points = points
        self.n_dims = n_dims
        self.n_points = n_points
        
    @cached_property
    def simplex_volumes(self):
        _pts = self.points[self.tri.simplices]
        dx = _pts[:, 1:] - _pts[:, [0]]
        vols = np.abs(np.linalg.det(dx)) * (1./6.)
        return vols
    
    @cached_property
    def vertex_volumes(self):
        vols = np.zeros(self.n_points, dtype=float)
        i_pts, simp_vols = self.tri.simplices, self.simplex_volumes
        self.__assign_volume(i_pts, simp_vols, vols)
        return vols
    
    @staticmethod
    @njit
    def __assign_volume(i_pts: np.ndarray, simp_vols: np.ndarray, 
                        vols: np.ndarray):
        n_simps, n_verts = i_pts.shape
        for i in range(n_simps):
            vols[i_pts[i]] += simp_vols[i] / n_verts
            
class ParticleVolume(abc.HasLog):
    def __init__(self, cell_iter: CellIter, **kw) -> None:
        super().__init__(**kw)
        self.cell_iter = cell_iter
        
    def run(self, boundary_thick=10, crange=None, fout_suffix=None):
        self.log('Start running')
            
        cell_iter = self.cell_iter
        snap = cell_iter.snap
        snap_dir = cell_iter.sim_info_m.snap_dir(snap)
        fout_name = snap_dir / 'particle_meta' / ('chunk.hdf5' + fout_suffix)
        
        with h5.File(fout_name, 'w') as f:
            
            g_cells = f.create_group('Cells')
            iter_x = cell_iter.iter_x_with_ngbs(
                boundary_thick=boundary_thick, crange=crange)
            for cid, x, mask in iter_x:
                
                n_p, n_in_cell = x.shape[0], mask.sum()
                self.log(f'Cell {cid}: {n_p=} {n_in_cell=}')
                
                vols = Triangulation(x).vertex_volumes
                assert len(vols) == len(x)
                
                g_cells.create_group(str(cid)).datasets.dump({
                    'volume': vols[mask]
                })
                
        self.log('Finished')