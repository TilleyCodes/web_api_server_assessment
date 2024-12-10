# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

import enum

class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    