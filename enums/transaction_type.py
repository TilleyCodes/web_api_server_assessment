# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

import enum

class TransactionType(enum.Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    BUY = "BUY"
    SELL = "SELL"
