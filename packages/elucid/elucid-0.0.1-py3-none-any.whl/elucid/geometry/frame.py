from __future__ import annotations
import typing
from typing import Self
from pyhipp_sims import sims
from pyhipp.core import abc
import numpy as np


class SimFrame(abc.HasDictRepr):

    repr_attr_keys = 'sim_info',

    def __init__(self, sim_info: sims.SimInfo | str, **base_kw):
        super().__init__(**base_kw)
        if isinstance(sim_info, str):
            sim_info = sims.predefined[sim_info]
        self.sim_info: sims.SimInfo = sim_info


class ComaLikeObsFrame(SimFrame):

    repr_attr_keys = SimFrame.repr_attr_keys + ('coma_pos_j2k',)

    def __init__(self, coma_pos_j2k: np.ndarray, **base_kw) -> None:
        super().__init__(**base_kw)

        coma_pos_j2k = np.array(coma_pos_j2k, dtype=float)
        coma_axes = self.projected_axes(coma_pos_j2k)

        self.coma_pos_j2k = coma_pos_j2k
        self.coma_axes = coma_axes

    @staticmethod
    def projected_axes(pos_target):
        norm = np.linalg.norm(pos_target)
        ax_z = pos_target / norm

        tmp_ax_y = np.array([0.0, 0.0, 1.0], dtype=float)

        ax_x = np.cross(tmp_ax_y, ax_z)
        ax_x /= np.linalg.norm(ax_x)

        ax_y = np.cross(ax_z, ax_x)

        return np.array([ax_x, ax_y, ax_z])


class SimFrameSdssL500(ComaLikeObsFrame):

    repr_attr_keys = ComaLikeObsFrame.repr_attr_keys + (
        'earth_pos_sim', 'phi0', 'j2k_axes', 'earth_axes',)

    def __init__(self, sim_info: sims.SimInfo | str = 'elucid',
                 coma_pos_j2k: np.ndarray = [-61.61415, -16.29136, 33.81053],
                 **base_kw):

        super().__init__(coma_pos_j2k=coma_pos_j2k,
                         sim_info=sim_info, **base_kw)

        phi0 = 39.0 * np.pi/180.0
        j2k_axes = np.array([
            [np.cos(phi0), np.sin(phi0), 0.0],
            [np.cos(phi0 + np.pi/2.0), np.sin(phi0 + np.pi/2.0), 0.0],
            [0.0, 0.0, 1.0]
        ], dtype=float)
        earth_axes = np.array([
            [np.cos(-phi0), np.sin(-phi0), 0.0],
            [np.cos(np.pi/2.0 - phi0), np.sin(np.pi/2.0 - phi0), 0.0],
            [0.0, 0.0, 1.0]], dtype=float)

        self.earth_pos_sim = np.array([370.0, 370.0, 30.0], dtype=float)
        self.phi0 = phi0
        self.j2k_axes = j2k_axes
        self.earth_axes = earth_axes

    def rebind_coma(self, coma_pos_j2k: np.ndarray) -> Self:
        return self.__class__(sim_info=self.sim_info,
                              coma_pos_j2k=coma_pos_j2k)

    def vel_sim_to_j2k(self, vel_sim: np.ndarray) -> np.ndarray:
        return np.matmul(vel_sim, self.j2k_axes.T)
    
    def los_vel(self, pos_sim: np.ndarray, vel_sim: np.ndarray) -> np.ndarray:
        pos, vel = self.pos_sim_to_j2k(pos_sim), self.vel_sim_to_j2k(vel_sim)
        return self.los_vel_from_j2k(pos, vel)
    
    def los_vel_from_j2k(self, x_j2k, v_j2k):
        x_unit = x_j2k / np.linalg.norm(x_j2k, axis=1, keepdims=True)
        v_los = (v_j2k * x_unit).sum(axis=1)
        return v_los

    def pos_sim_to_j2k(self, pos_sim: np.ndarray) -> np.ndarray:
        pos = pos_sim - self.earth_pos_sim
        return np.matmul(pos, self.j2k_axes.T)

    def pos_j2k_to_sim(self, pos_j2k: np.ndarray) -> np.ndarray:
        pos = np.matmul(pos_j2k, self.earth_axes.T)
        return pos + self.earth_pos_sim

    def pos_j2k_to_ra_dec_z(
            self, pos_j2k,
            z_finder='interp',
            interp_kw={'dz': 1.0e-2}) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        '''
        Return ra, dec and z.
        @z_finder: 'interp' or 'brute-force'
        '''
        assert z_finder in ['interp', 'brute-force']

        norm = np.linalg.norm(pos_j2k, axis=1, keepdims=True)
        norm[norm < 1.0e-10] = 1.0e-10

        pos_j2k_normed = pos_j2k / norm
        ra, dec = self.pos_spherical_to_ra_dec(pos_j2k_normed)

        if z_finder == 'interp':
            z = self.interp_cdis_to_z(self.sim_info, norm[:, 0], **interp_kw)
        else:
            z = self.sim_info.cosmology.redshifts.at_comoving(norm[:, 0])

        return ra, dec, z
    
    def pos_ra_dec_d_to_j2k(self, ra: np.ndarray, dec: np.ndarray,
                            d_c: np.ndarray) -> np.ndarray:
        j2k_u = self.pos_ra_dec_to_spherical(ra, dec)
        j2k = j2k_u * d_c[:, None]
        return j2k

    def pos_ra_dec_z_to_j2k(self, ra: np.ndarray, dec: np.ndarray,
                            z: np.ndarray) -> np.ndarray:
        j2k_u = self.pos_ra_dec_to_spherical(ra, dec)
        d = self.sim_info.cosmology.distances.comoving_at(z)
        j2k = j2k_u * d[:, None]
        return j2k

    def pos_j2k_to_coma(self, pos_j2k: np.ndarray) -> np.ndarray:
        pos = pos_j2k - self.coma_pos_j2k
        return np.matmul(pos, self.coma_axes.T)

    @staticmethod
    def interp_cdis_to_z(sim_info: sims.SimInfo, d: np.ndarray,
                         dz: float = 1.0e-2):
        assert d.min() >= 0

        cosm = sim_info.cosmology
        z_max = cosm.redshifts.at_comoving(d.max()) + 0.1
        zp = np.arange(0.0, z_max, step=dz, dtype=float)
        dp = cosm.distances.comoving_at(zp)

        z = np.interp(d, dp, zp)
        return z

    @staticmethod
    def pos_spherical_to_ra_dec(pos_spherical):
        '''
        Find RA, Dec in degree.
        norm of ``pos_spherical`` must be 1.0 in each row.
        '''

        dec = np.arcsin(pos_spherical[:, 2])
        ra = np.arctan2(pos_spherical[:, 1], pos_spherical[:, 0])

        sel = ra < 0.
        ra[sel] = ra[sel] + 2.0*np.pi

        ra *= 180.0 / np.pi
        dec *= 180.0 / np.pi

        return ra, dec

    @staticmethod
    def pos_ra_dec_to_spherical(ra: np.ndarray, dec: np.ndarray):

        ra, dec = ra * np.pi / 180.0, dec * np.pi / 180.0

        r = np.cos(dec)
        x0 = r * np.cos(ra)
        x1 = r * np.sin(ra)
        x2 = np.sin(dec)
        return np.column_stack([x0, x1, x2])
