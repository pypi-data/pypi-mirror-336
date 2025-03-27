from __future__ import annotations
from ..gen_util import fields
from .cell_storage import CellIter
from typing import Tuple
import numpy as np
from pyhipp.core import DataDict, abc
from pyhipp.io import h5
from .sim_info_for_elucid import SimInfo, SimInfoForElucid

class PaintDensityField(abc.HasLog):
    
    def __init__(self, field: fields.PeriodicField, 
                 painter: fields.MassAssigner,
                 **kw) -> None:
        
        super().__init__(*kw)
        
        self.field = field
        self.painter = painter
        
    def paint_cells(self, cell_iter: CellIter, crange: Tuple[int,int]):
        for cell in cell_iter(cell_iter.ld_spec_x, crange=crange):
            self.paint_cell(cell)
        
    def paint_cell(self, cell: DataDict):
        x = cell['ps/x']
        self.painter.add(self.field, x)
        
    def dump(self, g: h5.Group, field_dtype=np.float32):
        field, painter = self.field, self.painter
        ccfg, data = field.cell_cfg, field.data.astype(field_dtype)
        meta = {
            'n_grids': ccfg.n_grids,
            'l_box': ccfg.l_box,
            'painter_kind': painter.kind,
            'data': data
        }
        g.datasets.dump(meta)
        
        
class SmoothDensityField(abc.HasLog):
    def __init__(self, field: fields.PeriodicField, smoother: fields.Smoother, 
                 **kw) -> None:
        
        super().__init__(**kw)
        
        self.field = field
        self.smoother = smoother
        
    def run(self) -> None:
        self.field_result = self.smoother.run(self.field)
        
    def dump(self, g: h5.Group, field_dtype=np.float32):
        data = self.field_result.data.astype(field_dtype)
        g.datasets.create('data', data, flag='ac')
        
        
class LoadDensityField(abc.HasLog, abc.HasDictRepr):
    
    repr_attr_keys = 'meta', 'field'
    
    def __init__(self, sim_info: SimInfo, snap: int, 
                 sample='Raw', n_grids=512, smooth=None, 
                 mode = 'r', dtype=np.float64,
                 **kw):
        
        super().__init__(**kw)
        
        info_e = SimInfoForElucid(sim_info)
        fname = info_e.snap_dir(snap) / 'fields.hdf5'
        
        file = h5.File(fname, mode)
        group = file[f'{sample}/NumGrids_{n_grids}/Density']
        n_grids, l_box = group.datasets['n_grids', 'l_box']
        if smooth is not None:
            group = group[smooth]
        data = group.datasets['data'].astype(dtype)
        
        n_per_grid = data.mean()
        data /= n_per_grid
        ccfg = fields.CellConfig(n_grids, l_box)
        field = fields.PeriodicField(data=data, cell_cfg=ccfg)
        
        self.sim_info = sim_info
        self.sim_info_e = info_e
        self.file = file
        self.group = group
        self.field = field                      # density contrast field
        self.meta = DataDict({
            'fname': fname, 'snap': snap, 'sample': sample, 'n_grids': n_grids,
            'smooth': smooth, 'n_per_grid': n_per_grid
        })
        
    def close(self):
        del self.group
        self.file.close()
        
    def __enter__(self):
        return self
    
    def __exit__(self, *exc):
        self.close()
        
        