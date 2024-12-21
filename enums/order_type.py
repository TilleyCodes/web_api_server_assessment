"""
this module defines the OrderType enumeration for order types.
"""

import enum

class OrderType(enum.Enum):
    """
    Enum for order types.
    """
    BUY = "BUY"
    SELL = "SELL"
