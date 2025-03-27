from pyhipp.astro.cosmology.model import LambdaCDM
from dataclasses import dataclass
import numpy as np


class LinearPerturbationTheory:
    
    @dataclass
    class Policy:
        growth_rate_f_approx: str     = 'Lahav1991'   # 'Peebles1980', 'Lahav1991'

    
    def __init__(self, cosm: LambdaCDM, policy: Policy = None) -> None:
        self.cosm = cosm
        
        if policy is None:
            policy = LinearPerturbationTheory.Policy()
        self.policy = policy
    
    def growth_rate_f(self, z: np.ndarray) -> np.ndarray:
        cosm, pl = self.cosm, self.policy
        o_m = cosm.omega_m(z)
        f = o_m ** 0.6
        if pl.growth_rate_f_approx == 'Lahav1991':
            o_l = cosm.omega_l(z)
            f += o_l / 70. * (0.5 * o_m + 1.)
        elif pl.growth_rate_f_approx == 'Peebles1980':
            pass
        else:
            raise KeyError(f'Unknown growth rate approximation: '
                           f'{pl.growth_rate_f_approx}')
        return f
    