import decimal
import pandas as pd

try:
    import pandas_ta as _ta  # noqa
except ImportError:
    pass

from .proxies import SessionProxy as Session
from .strategy import Strategy
from .system import Cipher
from .values import base, percent, quote


pd.options.mode.chained_assignment = None  # default='warn'
decimal.getcontext().prec = 20
