from decimal import Decimal

from cipher.models import SimpleCommission, Time, Transaction
from cipher.values import percent


def test_simple_commission():
    commission = SimpleCommission(Decimal(1))
    assert commission.value == 1

    commission = SimpleCommission('1')
    assert isinstance(commission.value, Decimal)
    assert commission.value == 1

    commission = SimpleCommission(percent('0.1'))
    assert commission.value == Decimal('0.001')

    result = commission.for_transaction(
        Transaction(
            ts=Time.from_string('2020-01-01T01:01'),
            base=Decimal(10),
            quote=Decimal(20)
        )
    )
    assert result == Decimal('0.02')
