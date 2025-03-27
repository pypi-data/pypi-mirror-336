from pyhipp.core import abc
from typing import Any, Dict, Tuple
import numpy as np

class NumbaClassWrapper(abc.HasSimpleRepr):
    
    Impl: type                      = None
    impl_repr_items: Tuple          = None
    self_repr_items: Tuple          = None
    quantile_repr_items: Tuple      = None
    
    def __init__(self, impl: Impl, **kw) -> None:
        super().__init__(**kw)
        self.impl = impl
    
    @classmethod
    def create(cls, wrapper_kw: dict = None, **impl_kw):
        wrapper_kw, impl_kw = cls._parse_creator_kw(wrapper_kw, **impl_kw)
        return cls(cls.Impl(**impl_kw), **wrapper_kw)
    
    @classmethod
    def _parse_creator_kw(cls, wrapper_kw: dict = None, 
                         **kw) -> Tuple[Dict, Dict]:
        if wrapper_kw is None:
            wrapper_kw = {}
        impl_kw = {}
        for k, v in kw.items():
            if isinstance(v, NumbaClassWrapper):
                v = v.impl
            impl_kw[k] = v
        return wrapper_kw, impl_kw
    
    def to_simple_repr(self) -> dict:
        out = {
            'type': self.__class__.__name__,
        }
        items, impl = self.impl_repr_items, self.impl
        
        if items is not None: 
            for item in items:
                if isinstance(item, str):
                    out[item] = getattr(impl, item)
                else:
                    k, Wrapper = item
                    out[k] = Wrapper(getattr(impl, k)).to_simple_repr()
                
        items = self.self_repr_items
        if items is not None:
            for item in items:
                v = getattr(self, item)
                if isinstance(v, abc.HasSimpleRepr):
                    out[item] = v.to_simple_repr()
                else:
                    out[item] = repr(v)
            
        items = self.quantile_repr_items
        if items is not None:
            for item in items:
                v = out.pop(item)
                k = f'{item}(min, 0.16, 0.5, 0.84, max)'
                out[k] = self._get_repr_quantiles(v)
            
        return out
    
    @staticmethod
    def _get_repr_quantiles(values: np.ndarray) -> Tuple[np.ndarray]:
        min, max = values.min(0), values.max(0)
        qs = np.quantile(values, axis=0, q=(.16, .5, .84))
        return (min,) + tuple(qs) + (max,)