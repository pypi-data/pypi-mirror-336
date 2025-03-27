from numba.experimental import jitclass
import numpy as np
from ..gen_util.mesh import Mesh

class Solver:
    pass

@jitclass
class _FFTSolverAuxiliary:
    
    mesh: Mesh
    
    def __init__(self, mesh: Mesh) -> None:
        
        self.mesh = mesh
        
    def green_fn_at_ik(self, ik: np.ndarray) -> np.ndarray:
        '''
        @ik: integer indices of the grid points in k-space. The last dimension 
        is the dimensionality of the k-space. Other dimensions are batch.
        '''
        n, h = self.mesh.n_grids, self.mesh.l_grid
        n_comps = ik.shape[-1]
        
        f0 = 2.0 / (h*h)
        f1 = np.cos((2.0*np.pi/n) * ik).sum(-1) - n_comps
        f = f0 * f1
        
        sel_0k = (ik == 0).all(-1)
        f[sel_0k] = 1.

        return np.reciprocal(f)