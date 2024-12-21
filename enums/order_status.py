"""
this module defines the OrderStatus enumeration for order status.
"""

import enum

class OrderStatus(enum.Enum):
    """
    Enum for order status.
    """
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    