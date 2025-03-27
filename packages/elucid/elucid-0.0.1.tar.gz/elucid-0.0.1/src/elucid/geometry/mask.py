from pyhipp.io import h5
from pyhipp.core import abc
from pyhipp_sims import sims
import numpy as np
from functools import cached_property


class ReconstAreaMask(abc.HasDictRepr):

    repr_attr_keys = ('sim_info',)

    def __init__(self, sim_info: str | sims.SimInfo, **base_kw) -> None:
        super().__init__(**base_kw)

        if isinstance(sim_info, str):
            sim_info = sims.predefined[sim_info]

        self.sim_info: sims.SimInfo = sim_info

    def mask_value_at(self, x_sim: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def is_in_reconst_area(self, x_sim: np.ndarray) -> np.ndarray:
        raise NotImplementedError()


class ReconstAreaMaskSdssL500(ReconstAreaMask):

    repr_attr_keys = ReconstAreaMask.repr_attr_keys + ('f_selected',)

    def __init__(self, sim_info: str | sims.SimInfo = 'elucid',
                 mask_name='SDSS_reconstruction_area',
                 **base_kw) -> None:
        '''
        @mask_name: name of the mask in the supplementary data. Allowed 
        values: 
        - 'SDSS_reconstruction_area'.
        - 'SDSS_reconstruction_area_large'.
        '''

        super().__init__(sim_info=sim_info, **base_kw)

        sim_info = self.sim_info
        p_meta = (sim_info.root_dir / 'supplementary' /
                  'reconstruction_pipeline' / 'geometry.hdf5')
        mask = h5.File.load_from(p_meta, f'Masks/{mask_name}') > .9

        self.mask_reconst_area = mask

        L = sim_info.box_size
        N = mask.shape[0]
        assert mask.shape == (N, N, N)

        self.box_size = L
        self.n_grids = N
        self.cell_size = L/N
        self.f_selected = mask.sum() / mask.size

    def mask_value_at(self, x_sim: np.ndarray) -> np.ndarray:
        '''
        @x_sim: position(s) in the simulation frame. May be shifted (out-of-box) 
        at most one box size.
        '''
        N, L_cell = self.n_grids, self.cell_size
        mask = self.mask_reconst_area

        x_sim = np.asarray(x_sim)
        cid = np.floor(x_sim / L_cell + 0.5).astype(int)
        cid[cid < 0] += N
        cid[cid >= N] -= N

        assert np.all(cid >= 0)
        assert np.all(cid <= N)

        return mask[tuple(cid.T)]

    def is_in_reconst_area(self, x_sim: np.ndarray) -> np.ndarray:
        return self.mask_value_at(x_sim)


class _ReconstAreaMasks:
    @cached_property
    def small(self):
        return ReconstAreaMaskSdssL500(mask_name='SDSS_reconstruction_area')

    @cached_property
    def large(self):
        return ReconstAreaMaskSdssL500(
            mask_name='SDSS_reconstruction_area_large')

    @cached_property
    def small_n512(self):
        return ReconstAreaMaskSdssL500(
            mask_name='SDSS_reconstruction_area_N512')

    @cached_property
    def large_n512(self):
        return ReconstAreaMaskSdssL500(
            mask_name='SDSS_reconstruction_area_large_N512')


reconst_area_masks = _ReconstAreaMasks()
