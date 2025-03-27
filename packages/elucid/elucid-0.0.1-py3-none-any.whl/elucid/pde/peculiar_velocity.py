from numba import njit
from dataclasses import dataclass
from .field import OverdensityField, PeculiarVelocityField
from .. import gen_util as gu
from 
from . import theory
from .poisson import _FFTSolverAuxiliary
from pyhipp.core import abc
import numpy as np

class Predictor(abc.HasLog):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

class LPTPredictor(Predictor):
    '''
    Predictor using Linear Perturbation Theory (LPT).
    '''
    
    @dataclass
    class Policy:
        theory: theory.LinearPerturbationTheory
    
    def __init__(self, policy: Policy, **kw) -> None:
        
        super().__init__(**kw)
        
        self.policy = policy
        
    def predict(self, delta: OverdensityField,
                z: float):
        
        mesh = delta.mesh
        aux = _FFTSolverAuxiliary(mesh)
        n = mesh.n_grids
        n_half = n // 2
        n0, n1 = n, n
        n2 = n_half + 1
        k_base
        
        for i0 in range(n0):
            ik0 = i0 - n if i0 > n_half else i0
            for i1 in range(n1): 
                ik1 = i1 - n if i1 > n_half else i1
                for i2 in range(n2):
                    ik2 = i2 - n if i2 > n_half else i2
                    w = aux.window_at_ik(ik0, n_grids) * \
                        aux.window_at_ik(ik1, n_grids) * \
                        aux.window_at_ik(ik2, n_grids)
                    field[i0,i1,i2] *= 1.0 / w
        
        delta_k = delta.field_k.data
        v_k = v.field_k.data
        assert delta_k is not None and v_k is not None
        
        theory = self.policy.theory
        growth_f = theory.growth_rate_f(z)
        H = theory.cosm.big_hubble(z)
        a = 1.0 / (1.0 + z)
        
    def __predict(delta_k: np.ndarray, n: int, mesh: Mesh):
        
        
        
    