import decimal

try:
    import pandas_ta as _ta  # noqa
except ImportError:
    pass

from .models import Session
from .strategy import Strategy
from .system import Cipher
from .values import base, percent, quote


decimal.getcontext().prec = 20
