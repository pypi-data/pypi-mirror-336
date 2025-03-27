from .. import gen_util as gu
from dataclasses import dataclass
import numpy as np
from pyhipp.core import abc

@dataclass
class Policy:
    
    fft_policy: gu.fft.FFTPolicy    = gu.fft.FFTPolicy(variant='real')
    mass_assignment_method: str     = 'CIC'
    
    @property
    def mass_assignment_obj(self):
        cls = gu.mass_assignment.MassAssignment
        return cls.from_method(self.mass_assignment_method)
    
class BaseField(abc.HasLog):
    def __init__(self, mesh: gu.mesh.Mesh, 
                 field_x: gu.field.Field = None, 
                 field_k: gu.field.Field = None,
                 policy: Policy = None, 
                 **kw) -> None:
        
        assert field_x is not None or field_k is not None
        if policy is None:
            policy = Policy()
        
        super().__init__(**kw)
        
        self.mesh = mesh
        self.field_x = field_x
        self.field_k = field_k
        self.policy = policy
        
    def update_field_x(self):
        self.field_x = self.field_k.fft.backward
        return self
        
    def update_field_k(self):
        self.field_k = self.field_x.fft.forward
        return self
    
    def compensate_mass_assignment_shape(self):
        '''
        Work on field_k.
        '''
        self.policy.mass_assignment_obj.compensate_shape(self.field_k)
        return self

class OverdensityField(BaseField):
        
    @staticmethod
    def create_empty(mesh: gu.mesh.Mesh, dtype: np.dtype = np.float64, 
                     policy: Policy = None):
        if policy is None:
            policy = Policy()
        f = gu.field.ScalarField3D(mesh.n_grids, dtype=dtype, 
                                   fft_policy=policy.fft_policy)
        return OverdensityField(mesh, field_x=f, policy=policy)
        
    def normalize(self):
        '''
        Update self from mass field (or number field) to over density field.
        '''
        m = self.field_x.data
        m_mean = m.mean()
        m /= m_mean
        m -= 1.
        
        return self
    
    
class PeculiarVelocityField(BaseField):
        
    @staticmethod
    def create_empty(mesh: gu.mesh.Mesh, dtype: np.dtype = np.float64, 
                     policy: Policy = None):
        if policy is None:
            policy = Policy()
        f = gu.field.VectorField3D(mesh.n_grids, dtype=dtype,
                                   fft_policy=policy.fft_policy)
        return PeculiarVelocityField(mesh, field_x=f, policy=policy)
        

