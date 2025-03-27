from __future__ import annotations
from pyhipp.core import abc
from typing import Any, Dict, Tuple, List, Mapping, Union, Set, Sequence, Callable
import numpy as np
from functools import cached_property

class SelectedArgs(abc.HasSimpleRepr, abc.HasName):
    def __init__(self, mask: np.ndarray = None, 
                 ids: np.ndarray = None, size: int = None,
        **kw) -> None:
        
        super().__init__(**kw)
        
        self._mask = mask
        self._ids = ids
        self._size = size
        
    @classmethod
    def create_all(self, size: int):
        return SelectedArgs(mask = np.ones(size, dtype=bool))
    
    @classmethod
    def create_none(self, size: int):
        return SelectedArgs(mask = np.zeros(size, dtype=bool))
        
    def to_simple_repr(self) -> dict:
        return {
            'name': self.name,
            'mask': self.mask,
            'ids':  self.ids,
            'size': self.size,
        }
    
    @property
    def mask(self):
        mask = self._mask
        if mask is None:
            mask = self.ids_to_mask(self._ids, self._size)
            self._mask = mask
        return mask
    
    @property
    def ids(self):
        ids = self._ids
        if ids is None:
            mask = self._mask
            ids = self.mask_to_ids(mask)
            self._ids = ids
            self._size = len(mask)
        return ids
    
    @property
    def size(self):
        size = self._size
        if size is None:
            size = len(self._mask)
            self._size = size
        return size
    
    @cached_property
    def selected_size(self):
        if self._mask is not None:
            return self._mask.sum()
        assert self._ids is not None
        return len(self._ids)
    
    @property
    def preferred_args(self):
        if self._mask is not None:
            return self._mask
        assert self._ids is not None
        return self._ids
    
    def __call__(self, *x: np.ndarray) -> Any:
        assert len(x) > 0
        args = self.preferred_args
        if len(x) == 1:
            return x[0][args]
        return tuple(_x[args] for _x in x)
    
    def __len__(self):
        return self.size
            
    @staticmethod
    def mask_to_ids(mask: np.ndarray):
        return mask.nonzero()[0]
    
    @staticmethod
    def ids_to_mask(ids: np.ndarray, size: int):
        mask = np.zeros(size, dtype=bool)
        mask[ids] = True
        return mask

class Filter(abc.HasSimpleRepr, abc.HasName):
    
    def __init__(self, **kw) -> None:
    
        super().__init__(**kw)
        
    @staticmethod
    def create_and(spec: Union[Sequence[Tuple[Any, Any]], Mapping[Any, Any]]):
        fs = []
        if isinstance(spec, Mapping):
            spec = spec.items()
        for k, v in spec:
            if np.isscalar(v) or isinstance(v, str):
                f = FilterEq(k, v)
            elif isinstance(v, Sequence):
                assert len(v) == 2
                f = FilterRange(k, v)
            elif isinstance(v, Callable):
                f = FilterByFn(k, v)
            else:
                raise ValueError(f'Invalid spec: key={k}, value={v}')
            fs.append(f)
        return FilterAnd(fs)
        
    def to_simple_repr(self) -> dict:
        return {
            'name': self.name
        }
        
    def __call__(self, catalog: Mapping) -> SelectedArgs:
        raise NotImplementedError()
    
    def __or__(self, filter: Filter):
        return FilterOr([self, filter])
        
    def __and__(self, filter: Filter):
        return FilterAnd([self, filter])
  
    def __invert__(self):
        return FilterNegate(self)
   
        
class FilterAll(Filter):
    
    def __call__(self, catalog: Mapping) -> SelectedArgs:
        return SelectedArgs.create_all(len(catalog))
        
class FilterNone(Filter):
    def __call__(self, catalog: Mapping) -> SelectedArgs:
        return SelectedArgs.create_none(len(catalog))
        
class FilterEq(Filter):
    def __init__(self, key: str, value: Any, **kw) -> None:
        
        super().__init__(**kw)
        
        self.key = key
        self.value = value
        
    def to_simple_repr(self) -> dict:
        out = super().to_simple_repr()
        out['key'] = self.key
        out['value'] = self.value
        return out
        
    def __call__(self, catalog: Mapping) -> SelectedArgs:
        return SelectedArgs(mask = catalog[self.key] == self.value)
        
class FilterNe(Filter):
    def __init__(self, key: str, value: Any, **kw) -> None:
        
        super().__init__(**kw)
        
        self.key = key
        self.value = value
        
    def to_simple_repr(self) -> dict:
        out = super().to_simple_repr()
        out['key'] = self.key
        out['value'] = self.value
        return out
        
    def __call__(self, catalog: Mapping) -> SelectedArgs:
        return SelectedArgs(mask = catalog[self.key] != self.value)
    
class FilterRange(Filter):
    def __init__(self, key: str, range: Tuple[Any, Any], **kw) -> None:
        
        super().__init__(**kw)
        
        self.key = key
        self.range = range

    def to_simple_repr(self) -> dict:
        out = super().to_simple_repr()
        out['key'] = self.key
        out['range'] = self.range
        return out
        
    def __call__(self, catalog: Mapping) -> SelectedArgs:
        lb, ub = self.range
        val = catalog[self.key]
        mask = (val >= lb) & (val < ub)
        return SelectedArgs(mask = mask)
    
class FilterIn(Filter):
    def __init__(self, key: str, values: Union[Tuple[Any, ...], Set[Any]], 
                 **kw) -> None:
        
        super().__init__(**kw)
        
        self.key = key
        self.values = values
        
    def to_simple_repr(self) -> dict:
        out = super().to_simple_repr()
        out['key'] = self.key
        out['values'] = self.values
        return out
    
    def __call__(self, catalog: Mapping) -> SelectedArgs:
        mask = np.zeros(len(catalog), dtype=bool)
        vals_in = catalog[self.key]
        vals_set = self.values
        for i, val in enumerate(vals_in):
            mask[i] = val in vals_set
        return SelectedArgs(mask = mask)
        
class FilterByFn(Filter):
    def __init__(self, key: str, fn: Callable, **kw) -> None:
        super().__init__(**kw)
        
        self.key = key
        self.fn = fn
        
    def to_simple_repr(self) -> dict:
        out = super().to_simple_repr()
        out['key'] = self.key
        out['fn'] = self.fn
        return out
    
    def __call__(self, catalog: Mapping) -> SelectedArgs:
        val = catalog[self.key]
        mask = self.fn(val)
        return SelectedArgs(mask = mask)
        
        
class FilterList(Filter):
    def __init__(self, filters: List[Filter], **kw) -> None:
        
        super().__init__(**kw)
        
        self.filters = [f for f in filters]
        
    def __len__(self):
        return len(self.filters)
    
    def to_simple_repr(self) -> dict:
        out = super().to_simple_repr()
        out['list'] = [f.to_simple_repr() for f in self.filters]
        return out
        
class FilterAnd(FilterList):
    def __call__(self, catalog: Mapping) -> SelectedArgs:
        if len(self) == 0:
            return SelectedArgs.create_all(len(catalog))
        fs = self.filters
        f0, fs = fs[0], fs[1:]
        mask = f0(catalog).mask
        for f in fs:
            mask &= f(catalog).mask
        return SelectedArgs(mask = mask)
    
class FilterOr(FilterList):
    def __call__(self, catalog: Mapping) -> SelectedArgs:
        if len(self) == 0:
            return SelectedArgs.create_none(len(catalog))
        fs = self.filters
        f0, fs = fs[0], fs[1:]
        mask = f0(catalog).mask
        for f in fs:
            mask |= f(catalog).mask
        return SelectedArgs(mask = mask)
    
class FilterNegate(Filter):
    def __init__(self, filter: Filter, **kw) -> None:
        
        super().__init__(**kw)
        self.filter = filter
        
    def __call__(self, catalog: Mapping) -> SelectedArgs:
        mask = self.filter(catalog).mask
        return SelectedArgs(mask = ~mask)