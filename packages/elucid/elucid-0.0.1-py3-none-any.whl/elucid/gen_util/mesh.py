from __future__ import annotations
from numba.experimental import jitclass
import numpy as np

@jitclass
class Mesh:
    
    n_grids: int
    l_box:  float
    l_grid: float
    
    def __init__(self, n_grids: int, l_box: float) -> None:
        l_grid = l_box / n_grids
        
        self.n_grids = n_grids
        self.l_box = l_box
        self.l_grid = l_grid