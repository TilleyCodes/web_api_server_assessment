"""
this moudule defines the TransactionType enumeration for transaction types.
"""

import enum

class TransactionType(enum.Enum):
    """
    Enum for transaction types.
    """
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    BUY = "BUY"
    SELL = "SELL"
