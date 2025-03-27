import numpy as np
from pyhipp.stats.random import Rng
from . import mesh
from . import field

class Points:
    
    def __init__(self, rng: Rng = None, l_box = 100.0, v_ub = 1.0e3, 
                 mass_ub = 1.0) -> None:
    
        if rng is None:
            rng = Rng()
            
        self.rng = rng
        self.l_box = l_box
        self.v_ub = v_ub
        self.mass_ub = mass_ub
        
    def get_n(self, n = 10000):
        x = self.rng.uniform(high=self.l_box, size=(n, 3))
        v = self.rng.uniform(high=self.v_ub, size=(n, 3))
        mass = self.rng.uniform(high=self.mass_ub, size=(n,))
        return x, v, mass
    
    def get_stacked_n(self, n = 10000):
        x, v, mass = self.get_n(n)
        out = np.empty((n, 4), dtype=np.float64)
        out[:, 0] = mass
        out[:, 1:] = mass[:, None] * v
        return x, out

class MeshedPoints(Points):
    def __init__(self, n_grids = 8, **kw) -> None:
        super().__init__(**kw)
        self.n_grids = n_grids
                    
    def mesh(self):
        return mesh.Mesh(self.n_grids, self.l_box)
    
    def field(self, n_comps = None):
        if n_comps is None:
            return field.ScalarField3D(self.n_grids)
        else:
            return field.VectorField3D(self.n_grids, n_comps)