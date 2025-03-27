import scipy.fft as scipy_fft
from dataclasses import dataclass, replace
import numpy as np
from typing import Tuple

@dataclass
class FFTPolicy:
    
    '''
    @shape: shape of the input array. If larger than input, pad input with 
            zeros; if smaller, crop.
    @axes: target axes to transform. Default: all axes, or last len(shape) axes 
           if specified shape. A repeated axis will be transformed multiple times.
    @norm: 'forward' | 'backward' | 'ortho' | None (means 'backward').
    @overwrite_input: whether input can be overwritten as temporary space.
    @n_workers: number of workers for parallel computation. Negative for a wrap 
                around from os.cpu_count().
    @variant: 'real' | 'complex'
    '''
    
    shape: Tuple[int,...]   = None
    axes: Tuple[int,...]    = None
    norm: str               = None
    overwrite_input: bool   = False
    n_workers: int          = None
    variant: str            = 'real'
    
    def forward(self, x: np.ndarray) -> np.ndarray:    
        fn = scipy_fft.rfftn if self.variant == 'real' else scipy_fft.fftn
        return fn(x, **self.__fftn_kw)
        
    def backward(self, x: np.ndarray) -> np.ndarray:
        fn = scipy_fft.irfftn if self.variant == 'real' else scipy_fft.ifftn
        return fn(x, **self.__fftn_kw)
    
    def replaced(self, **changes):
        return replace(self, **changes)
    
    @property
    def __fftn_kw(self):
        return dict(s=self.shape, axes=self.axes, norm=self.norm, 
            overwrite_x=self.overwrite_input, workers=self.n_workers)
        
        
default_fft_policy = FFTPolicy()