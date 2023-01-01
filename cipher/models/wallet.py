from decimal import Decimal
from typing import Dict

from pydantic import BaseModel


class Wallet(BaseModel):
    assets: Dict[str, Decimal]
