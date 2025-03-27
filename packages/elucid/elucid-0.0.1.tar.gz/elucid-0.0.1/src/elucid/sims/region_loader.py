from __future__ import annotations
import typing
from typing import Self
from pyhipp.io import h5
from functools import cached_property
import numpy as np
from .peano import Peano


class SnapshotStorage:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.f = h5.File(self.file_name, 'r')
        self.dm = self.f['PartType1']

    @cached_property
    def cell_filling_exp(self):
        '''
        The exponent p, where 2**p gives the number of cells along one side of 
        the box, N_side.
        '''
        return int(self.dm['CellFillingExp'][()])

    @cached_property
    def cell_filling_curve(self):
        p = self.cell_filling_exp
        curve = Peano(p)
        return curve

    @cached_property
    def l_box(self):
        '''
        Box size, L_box.
        '''
        return self.f['BoxSize'][()]

    @cached_property
    def cell_n_ps(self):
        '''
        No of particles in each cell.
        '''
        return self.dm['NumPartInCells'][()]

    @cached_property
    def n_cells(self):
        '''
        No of cells, N_cells = N_side**3.
        '''
        return len(self.cell_n_ps)

    @cached_property
    def n_cells_side(self):
        '''
        N_side = 2**p.
        '''
        return 2**self.cell_filling_exp

    @cached_property
    def l_cell(self):
        '''
        Cell side length.
        '''
        return self.l_box / self.n_cells_side

    @cached_property
    def tot_n_ps(self):
        '''
        Total number of particles.
        '''
        return self.cell_n_ps.sum()

    @cached_property
    def cell_p_offs(self):
        '''
        Offset of the first particle in each cell.
        Sized N_cells + 1, with the last element being the total number of
        particles.
        '''
        off = np.concatenate(([0], np.cumsum(self.cell_n_ps)))
        return off

    def cell_p_off(self, i_cell: int):
        '''
        Offset of the first particle, and 1 + the offset of the last particle
        in the cell indexed i_cell (PH index).
        '''
        p_offs = self.cell_p_offs
        return p_offs[i_cell], p_offs[i_cell + 1]

    def load_range(self, b: int, e: int, key='Coordinates'):
        '''
        Load a contiguous chunk of particles globally indexed in [b, e).
        '''
        return self.dm[key][b:e]

    def cell(self, i_cell: int):
        '''
        Return a loader for the cell indexed i_cell (PH index).
        '''
        return CellStorage(self, i_cell)

    def cell_batch(self, i_cells: np.ndarray, d_max_batch=32):
        '''
        Return a loader for a batch of cells indexed ``i_cells`` (PH index).
        '''
        return CellBatchStorage(self, i_cells, d_max_batch)

    def rect_region(self, x0: np.ndarray, dx: np.ndarray):
        '''
        Return a loader for a rectangular region defined by the center x0 and
        half side length dx along each dimension. 
        
        Periodic boundary conditions are applied.
        '''
        x0, dx = np.asarray(x0), np.asarray(dx)
        
        x_lo, x_hi = x0 - dx, x0 + dx
        l_cell, n_cells_side = self.l_cell, self.n_cells_side
        i_lo, i_hi = np.floor(x_lo / l_cell).astype(int), \
            np.floor(x_hi / l_cell).astype(int)
        i0, i1, i2 = [np.arange(_l, _h+1) % n_cells_side
                      for _l, _h in zip(i_lo, i_hi)]
        i0, i1, i2 = np.meshgrid(i0, i1, i2, indexing='ij')
        cid_3 = np.column_stack((i0.ravel(), i1.ravel(), i2.ravel()))
        cid_1 = np.array(self.cell_filling_curve.peano_hilbert_keys(cid_3))

        return CellBatchStorage(self, cid_1)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.f.close()


class CellBatchStorage:
    '''
    Loader of data for a batch of cells indexed ``i_cells`` (PH index).
    
    Note that additional cells may be loaded to avoid multiple small reads.
    @d_max_batch: maximum difference in the PH index for two cells to be loaded,
    along with the cells between them, by a single call
    '''

    def __init__(self, snap_sto: SnapshotStorage, i_cells: np.ndarray,
                 d_max_batch=32):
        i_cells = np.sort(i_cells)

        self.snap_sto = snap_sto
        self.i_cells = i_cells
        self.d_max_batch = d_max_batch

    def iter(self, key='Coordinates'):
        i_cells, d_max = self.i_cells, self.d_max_batch
        c0 = c1 = i_cells[0]
        for i_cell in i_cells[1:]:
            if i_cell < c1 + d_max:
                c1 = i_cell
                continue
            yield self._load_between(c0, c1, key)
            c0 = c1 = i_cell
        yield self._load_between(c0, c1, key)

    def _load_between(self, c0, c1, key='Coordinates'):
        sto = self.snap_sto
        b = sto.cell_p_off(c0)[0]
        e = sto.cell_p_off(c1)[1]
        return sto.load_range(b, e, key)


class CellStorage:
    '''
    Loader of data for a single cell.
    '''

    def __init__(self, snap_sto: SnapshotStorage, i_cell: int):
        self.snap_sto = snap_sto
        self.i_cell = i_cell
        self.p_beg, self.p_end = snap_sto.cell_p_off(i_cell)

    @cached_property
    def x(self):
        b, e = self.p_beg, self.p_end
        return self.snap_sto.load_range(b, e, 'Coordinates')
