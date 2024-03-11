from machine import Pin, SPI
import utime
import urandom
import ubinascii
from encryption import aes_cmac
from constants import *

class LoRa:
    def __init__(self, spi_channel, sck, mosi, miso, cs, rst, dio):
        self._spi = SPI(spi_channel, 4000000, 
            sck=Pin(sck), 
            miso=Pin(miso), 
            mosi=Pin(mosi))

        self._dio = Pin(irq, Pin.IN, Pin.PULL_UP)
        self._cs = Pin(cs, Pin.OUT, value=0)
        self._rst = Pin(rst, Pin.OUT, value=0)

        ### Reset SX1276
        self._rst.value(1)
        utime.sleep_ms(10)
        self._rst.value(0)
        


lora = LoRa(spi_channel=1, sck=10, mosi=11, miso=12, cs=14, rst=15, dio=18)
