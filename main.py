from machine import Pin, SPI, I2C
from ILI9341 import LCD_28_ILI9341
from touch import FT6336
from gui_manager import GUIManager
from home_page import HomePage
from prayer_page import PrayerPage
from quran_page import QuranPage
from audio_page import AudioPage
from settings_page import SettingsPage
import time

LCD_CS = 10
LCD_RS = 46
LCD_SCK = 12
LCD_MOSI = 11
LCD_MISO = 13
LCD_BL = 45

spi = SPI(
    2,
    baudrate=40000000,
    sck=Pin(LCD_SCK),
    mosi=Pin(LCD_MOSI),
    miso=Pin(LCD_MISO)
)

lcd = LCD_28_ILI9341(
    spi,
    cs=LCD_CS,
    rs=LCD_RS,
    blk=LCD_BL
)

i2c = I2C(
    0,
    scl=Pin(15),
    sda=Pin(16),
    freq=400000
)

touch = FT6336(
    i2c,
    rst=18,
    width=320,
    height=240
)

touch.TP_Set_Rotation(3)

gui = GUIManager(lcd, touch)

gui.register_page("home", HomePage())
gui.register_page("prayer", PrayerPage())
gui.register_page("quran", QuranPage())
gui.register_page("audio", AudioPage())
gui.register_page("settings", SettingsPage())

gui.show("home")

print("GUI started")

while True:
    if touch.TP_Get_Touch():
        x = touch.tp_x[0]
        y = touch.tp_y[0]

        print("Touch:", x, y)

        gui.handle_touch(x, y)

        time.sleep_ms(300)

    time.sleep_ms(50)