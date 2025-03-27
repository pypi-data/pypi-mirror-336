from __future__ import annotations
import numpy as np
from typing import Union, Sequence, Tuple
from .fft import FFTPolicy
    
class Field:

    Shape = Tuple[int, ...]
    
    class FFTContext:
        def __init__(self, policy: FFTPolicy, field: Field) -> None:
            self.policy = policy
            self.field = field
            
        @property
        def field_type(self):
            return type(self.field)
        
        @property
        def forward(self) -> Field:
            pl, field = self.policy, self.field
            data = pl.replaced(axes=field.axes).forward(field.data)
            return self.field_type(data = data, fft_policy=self.policy)
        
        @property
        def backward(self) -> Field:
            pl, field = self.policy, self.field
            data = pl.replaced(axes=field.axes).backward(field.data)
            return self.field_type(data = data, fft_policy=self.policy)

    def __init__(self, data: np.ndarray, fft_policy: FFTPolicy = None) -> None:
        
        self.data = data
        
        if fft_policy is None:
            fft_policy = FFTPolicy()
            
        self.fft_policy = fft_policy
        
    @property
    def fft(self):
        return type(self).FFTContext(self.fft_policy, self)
    
    @property
    def dtype(self) -> np.dtype:
        return self.data.dtype
    
    @property
    def data_n_dims(self) -> int:
        return self.data.ndim
    
    @property
    def data_shape(self) -> Field.Shape:
        return self.data.shape

    @property
    def n_dims(self) -> int:
        raise NotImplementedError()
    
    @property
    def shape(self) -> Field.Shape:
        raise NotImplementedError()
    
    @property
    def axes(self) -> Tuple[int,...]:
        return np.arange(self.n_dims)
    
    @property
    def imag(self) -> Field:
        return type(self)(data=self.data.imag, fft_policy=self.fft_policy)
    
    @property
    def real(self) -> Field:
        return type(self)(data=self.data.real, fft_policy=self.fft_policy)
    
    def __repr__(self) -> str:
        data_shape, dtype = self.data_shape, self.dtype
        name = type(self).__name__
        return f'{name}({data_shape=}, {dtype=})'


class ScalarField(Field):
    @property
    def n_dims(self) -> int:
        return self.data.ndim
            
    @property
    def shape(self) -> Field.Shape:
        return self.data.shape
    
    def __repr__(self) -> str:
        shape, dtype = self.shape, self.dtype
        name = type(self).__name__
        return f'{name}({shape=}, {dtype=})'

class ScalarField3D(ScalarField):
    def __init__(self, 
                 shape: Union[int, Field.Shape] = None, 
                 dtype = np.float64, 
                 data: np.ndarray = None, **kw) -> None:
        if data is None:
            if np.isscalar(shape):
                shape = (shape,) * 3
            assert len(shape) == 3
            data = np.zeros(shape, dtype=dtype)
        
        super().__init__(data, **kw)
        

class VectorField(Field):
    
    ScalarField = ScalarField    
    
    @classmethod
    def from_comps(cls, comps: Sequence[ScalarField]):
        return cls(data=np.stack([comp.data for comp in comps], axis=-1))
    
    @property
    def n_dims(self) -> int:
        return self.data.ndim - 1
    
    @property
    def shape(self) -> Field.Shape:
        return self.data.shape[:-1]
    
    @property
    def n_comps(self) -> int:
        return self.data.shape[-1]
    
    def comp(self, i: int):
        return type(self).ScalarField(data=self.data[...,i], 
                fft_policy=self.fft_policy)
    
    @property
    def comps(self):
        return (self.comp(i) for i in range(self.n_comps))
        
    def __repr__(self) -> str:
        shape, n_comps, dtype = self.n_comps, self.shape, self.dtype
        name = type(self).__name__
        return f'{name}({shape=}, {n_comps=}, {dtype=})'
    
class VectorField3D(VectorField):

    ScalarField = ScalarField3D

    def __init__(self, 
                 shape: Union[int, Field.Shape] = None, 
                 n_comps = 3,
                 dtype = np.float64,
                 data: np.ndarray = None, **kw) -> None:
        if data is None:
            if np.isscalar(shape):
                shape = (shape,) * 3
            assert len(shape) == 3
            data = np.zeros((*shape, n_comps), dtype=dtype)
            
        super().__init__(data, **kw)
    
