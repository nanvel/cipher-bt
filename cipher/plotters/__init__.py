from .base import Plotter
from .finplot import FinplotPlotter
from .mplfinance import MPLFinancePlotter


PLOTTERS = {
    "finplot": FinplotPlotter,
    "mplfinance": MPLFinancePlotter,
}


__all__ = ("Plotter", "PLOTTERS")
