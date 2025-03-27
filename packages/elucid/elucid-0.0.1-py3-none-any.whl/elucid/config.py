from __future__ import annotations
import os
from pyhipp_sims import sims
from pathlib import Path
from pyhipp import plot
from pyhipp.core import DataDict

plot.runtime_config.use_stylesheets('mathtext-it')

class ColorSets:
    dark2 = plot.ColorSeq.predefined('dark2').get_rgba()
    tab10 = plot.ColorSeq.predefined('dark2').get_rgba()
    set1 = plot.ColorSeq.predefined('set1').get_rgba()
    set2 = plot.ColorSeq.predefined('set2').get_rgba()

class ProjPaths:
    proj_dir = Path(os.environ['MAHGIC_WORK_DIR']
                    ).resolve() / 'data' / 'elucid'
    
    sims_dir = proj_dir / 'sims'
    obs_dir = proj_dir / 'obs'
    figs_dir = proj_dir / 'figures'

    @staticmethod
    def sim_dir_of(sim_info: sims.SimInfo) -> Path:
        return ProjPaths.sims_dir / sim_info.name

    @staticmethod
    def save_fig(file_name: str, **savefig_kw):
        plot.savefig(ProjPaths.figs_dir / file_name, **savefig_kw)
