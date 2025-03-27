"""M5 hardware module"""

from .pin import Pin
from .i2c import I2C
from .uart import UART
from .speaker import Speaker

__all__ = ['Pin', 'I2C', 'UART', 'Speaker']