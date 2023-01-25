from ..utils import in_notebook
from .base import Plotter
from .finplot import FinplotPlotter
from .mplfinance import MPLFinancePlotter


PLOTTERS = {
    "finplot": FinplotPlotter,
    "mplfinance": MPLFinancePlotter,
}


def get_default_plotter():
    if in_notebook:
        plotter = MPLFinancePlotter
    else:
        plotter = FinplotPlotter
        try:
            plotter.check_requirements()
        except RuntimeError:
            plotter = MPLFinancePlotter

    return plotter


__all__ = ("get_default_plotter", "Plotter", "PLOTTERS")
