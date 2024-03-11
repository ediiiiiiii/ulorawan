import utime
from ulora import TTN, uLoRa
from machine import Pin
# Refer to device pinout / schematics diagrams for pin details
LORA_CS = const(14)
LORA_SCK = const(10)
LORA_MOSI = const(11)
LORA_MISO = const(12)
LORA_IRQ = const(18)
LORA_RST = const(15)
LORA_DATARATE = "SF12BW125"  # Choose from several available
# From TTN console for device
DEVADDR = bytearray([0x26, 0x0B, 0x59, 0xA0])
NWKEY = bytearray([0x58, 0x00, 0x9D, 0xC6, 0x17, 0x19, 0x4F, 0x77, 0x63, 0xC5, 0x2C, 0x28, 0xCB, 0xFA, 0x78, 0x4D])
APP = bytearray([0x14, 0x95, 0x0A, 0x41, 0xA8, 0x30, 0xDF, 0x12, 0x45, 0x2F, 0x97, 0x78, 0x43, 0x7F, 0x08, 0xB9])


JOIN_EUI = bytearray([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])
DEV_EUI = bytearray([0x70, 0xB3, 0xD5, 0x7E, 0xD0, 0x06, 0x59, 0xD1])
APP_KEY = bytearray([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])

TTN_CONFIG = TTN(DEVADDR, NWKEY, APP, country="EU")
FPORT = 1
lora = uLoRa(
    cs=LORA_CS,
    sck=LORA_SCK,
    mosi=LORA_MOSI,
    miso=LORA_MISO,
    irq=LORA_IRQ,
    rst=LORA_RST,
    ttn_config=TTN_CONFIG,
    datarate=LORA_DATARATE,
    fport=FPORT
)
data = bytearray([1,2,3,4])
# ...Then send data as bytearray

def blink():
    led = Pin("LED", Pin.OUT, value=1)
    utime.sleep_ms(50)
    led.value(0)
utime.sleep_ms(1000)
blink()
utime.sleep_ms(100)
blink()

for i in range(100):
    lora.join(DEV_EUI, JOIN_EUI, APP_KEY)
    utime.sleep_ms(2000)
