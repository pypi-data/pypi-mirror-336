from __future__ import annotations
import typing
from typing import Self
import numpy as np
import numba
from numba.experimental import jitclass
from pyhipp.field.neighbor import kd_mesh
from pyhipp.io import h5
from pyhipp_sims.sims import trees, snapshots, predefined
from pathlib import Path


def halomass2radius(m, z):
    zp1 = z + 1.
    o_m = 0.258
    o_l = 0.742
    rho_c_0 = 277536627245.83075
    e_val = np.sqrt(zp1*zp1*zp1*o_m + o_l)
    rho = rho_c_0 * e_val * e_val * 200
    r = pow(m * 3. / 4. / 3.1415 / rho, 1. / 3.) * zp1
    return r


def take_subhalos_from_tree(
        file_id: int, dst_snaps: np.ndarray, m_h_lb: float,
        o_path: Path):

    ld = trees.TreeLoaderElucidRaw(file_id)

    M200c = ld['m_crit200']
    Vmax = ld['v_max']
    Pos = ld['x']
    TreeID = ld['tree_id']
    FOFFirst = ld['f_in_grp']
    SnapNum = ld['snap']
    is_c = ld['is_c']
    z = ld.sim_info.redshifts[SnapNum]
    R200c = halomass2radius(M200c*1.0e10, z)
    FileID = np.full_like(TreeID, file_id)
    l_box = ld.sim_info.full_box_size
    Pos[Pos < 0.] += l_box
    Pos[Pos >= l_box] -= l_box
    assert np.all((Pos >= 0.) & (Pos < l_box))

    sel_0 = is_c & (M200c > m_h_lb)
    outs = {}
    for dst_snap in dst_snaps:
        sel = sel_0 & (SnapNum == dst_snap)
        outs[str(dst_snap)] = {
            'M200c': M200c[sel],
            'R200c': R200c[sel],
            'Vmax': Vmax[sel],
            'Pos': Pos[sel],
            'FileID': FileID[sel],
            'TreeID': TreeID[sel],
            'FOFFirst': FOFFirst[sel],
        }
    h5.File.dump_to(o_path, outs, f_flag='w')


def gather_subhalos_by_snap(paths, snap, o_path):
    subhalos = {}
    for p in paths:
        d = h5.File.load_from(p, key=str(snap))
        for k, v in d.items():
            subhalos.setdefault(k, []).append(v)
    subhalos = {
        k: np.concatenate(v) for k, v in subhalos.items()
    }
    h5.File.dump_to(o_path, subhalos, f_flag='w')

@jitclass
class HaloProfiles:
    xs: numba.float64[:, :]
    rs: numba.float64[:]
    n_hs: int
    l_box: float

    n_rs: int
    lr_min: float
    lr_max: float
    dlr: float

    profs: numba.float64[:, :]
    mv1: numba.float64[:]
    mcnt: numba.float64[:]

    def __init__(self, xs, rs, l_box, n_rs=20, lr_min=-2., lr_max=0.):
        assert len(xs) == len(rs)
        n_hs = len(xs)

        self.xs = xs
        self.rs = rs
        self.n_hs = n_hs
        self.l_box = l_box

        dlr = (lr_max - lr_min) / n_rs
        self.n_rs = n_rs
        self.lr_min = lr_min
        self.lr_max = lr_max
        self.dlr = dlr

        self.profs = np.zeros((n_hs, n_rs), dtype=np.float64)
        self.mv1 = np.zeros(n_hs, dtype=np.float64)
        self.mcnt = np.zeros(n_hs, dtype=np.float64)

    def on(self, i_h, xs_ngbs):
        x_h, r_h = self.xs[i_h], self.rs[i_h]
        l_box = self.l_box
        l_half = l_box * 0.5
        lr_min, dlr, n_rs = self.lr_min, self.dlr, self.n_rs
        r_max = 10.0**self.lr_max
        for x_ngb in xs_ngbs:
            dx_sq = 0.
            for dx in x_ngb - x_h:
                if dx > l_half:
                    dx -= l_box
                elif dx < -l_half:
                    dx += l_box
                dx_sq += dx * dx
            dr = np.sqrt(dx_sq)
            if dr <= r_h:
                self.mv1[i_h] += dr
                self.mcnt[i_h] += 1.0
            if dr < r_max:
                lr = np.log10(dr / r_h + 1.0e-9)
                i_r = np.int64(np.floor((lr - lr_min)/dlr))
                if i_r >= 0 and i_r < n_rs:
                    self.profs[i_h, i_r] += 1.0


def find_profile(path: Path, snap, file_ids: np.ndarray):
    info = predefined['elucid']
    l_box = info.full_box_size
    n_grids = 512
    mesh = kd_mesh._PE3Mesh(l_box, n_grids)

    with h5.File(path) as f:
        x_hs, r_hs, m_hs = f.datasets['Pos', 'R200c', 'M200c']
        x_hs, r_hs, m_hs = np.asarray(x_hs, dtype=np.float64), \
            np.asarray(r_hs, dtype=np.float64), \
            np.asarray(m_hs, dtype=np.float64)
    profs = HaloProfiles(x_hs, r_hs, l_box)

    for file_id in file_ids:
        print(f'Processing {file_id=}', flush=True)
        ld = snapshots.SnapshotLoaderElucidRaw(
            info, snap=snap, chunk_id=file_id)
        xs = np.asarray(ld.load_particles('x'), dtype=np.float64)
        xs[xs < 0.] += l_box
        xs[xs >= l_box] -= l_box
        kd = kd_mesh._PE3_from_meshing_points(mesh, xs)
        kd.query_points(profs)
        m_p = ld.part_mass_dm
    print(f'Part mass: {m_p}', flush=True)

    mcnt = profs.mcnt * m_p
    pfs = profs.profs * m_p
    mv1 = profs.mv1 * m_p / m_hs

    h5.File.dump_to(path, {
        'MassVariance1': mv1,
        'MCnt': mcnt,
        'Prof': pfs,
        # ConcFit = ld[]
    }, dump_flag='ac')
