from machine import I2C, Pin
import time

ADDR = 0x18
SCL = 15
SDA = 16
AMP_EN = 1


class ES8311:
    def __init__(self):
        self.i2c = I2C(0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)
        self.amp = Pin(AMP_EN, Pin.OUT)

    def w(self, reg, val):
        self.i2c.writeto_mem(ADDR, reg, bytes([val]))

    def r(self, reg):
        return self.i2c.readfrom_mem(ADDR, reg, 1)[0]

    def init(self):
        print("Initializing ES8311 codec...")

        # Enable speaker amp, LOW = enable
        self.amp.value(0)

        # Reset
        self.w(0x00, 0x1F)
        time.sleep_ms(20)
        self.w(0x00, 0x80)   # power state machine on
        time.sleep_ms(20)

        # Clock: use BCLK as clock source, enable BCLK + DAC clocks
        self.w(0x01, 0xB4)   # MCLK_SEL=BCLK, MCLK_ON, BCLK_ON, DAC clocks on
        self.w(0x02, 0x00)
        self.w(0x03, 0x10)
        self.w(0x04, 0x10)
        self.w(0x05, 0x00)
        self.w(0x06, 0x00)
        self.w(0x07, 0x00)
        self.w(0x08, 0xFF)

        # I2S input, 16-bit, I2S format
        self.w(0x09, 0x0C)

        # Power up analog + DAC
        self.w(0x0D, 0x01)
        self.w(0x0E, 0x02)
        self.w(0x0F, 0x00)
        self.w(0x10, 0x1F)
        self.w(0x11, 0x7F)
        self.w(0x12, 0x00)   # DAC power up
        self.w(0x13, 0x10)   # enable output
        self.w(0x31, 0x00)   # DAC unmute
        self.w(0x32, 0xFF)   # high volume
        self.w(0x37, 0x08)

        print("ES8311 codec initialized")

    def unmute(self):
        self.w(0x31, 0x00)

    def set_volume(self, value=0xFF):
        self.w(0x32, value)