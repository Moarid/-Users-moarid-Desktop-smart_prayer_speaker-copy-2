import time
from machine import Pin, SPI
from ILI9341 import LCD_28_ILI9341
from Font_8x16_EN import Font_8x16_EN
from Font_12x24_EN import Font_12x24_EN

BLACK  = 0x0000
WHITE  = 0xFFFF
RED    = 0xF800
GREEN  = 0x07E0
BLUE   = 0x001F
YELLOW = 0xFFE0
GRAY   = 0x8410
CYAN   = 0x07FF

LCD_CS = 10
LCD_RS = 46
LCD_SCK = 12
LCD_MOSI = 11
LCD_MISO = 13
LCD_BL = 45

lcd = None

PRAYERS = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]


def init():
    global lcd

    spi = SPI(
        2,
        baudrate=40000000,
        sck=Pin(LCD_SCK),
        mosi=Pin(LCD_MOSI),
        miso=Pin(LCD_MISO)
    )

    lcd = LCD_28_ILI9341(spi, LCD_CS, LCD_RS, LCD_BL)

    try:
        lcd.LCD_Set_Rotate(1)  # landscape
    except:
        pass

    lcd.Show_BMP_Pic("/background.bmp", 0, 0)
    print("LCD ready")


def fill(x, y, w, h, color):
    if lcd:
        lcd.Fill_Rect(x, y, w, h, color)


def text(x, y, value, color=WHITE, bg=BLACK, big=False):
    if not lcd:
        return
    font = Font_12x24_EN if big else Font_8x16_EN
    try:
        lcd.Show_String(x, y, str(value), font, color, bg)
    except Exception as e:
        print("Text error:", e)

def clean_time(value):
    return str(value)[:5]


def time_to_minutes(value):
    h, m = value[:5].split(":")
    return int(h) * 60 + int(m)


def current_minutes():
    now = time.localtime()
    return now[3] * 60 + now[4]


def get_next_prayer(prayer_times):
    now = current_minutes()

    for prayer in PRAYERS:
        if prayer in prayer_times:
            p_time = clean_time(prayer_times[prayer])
            if time_to_minutes(p_time) >= now:
                return prayer, p_time

    return "Fajr", clean_time(prayer_times.get("Fajr", "--:--"))


def show_boot():
    if not lcd:
        return

    lcd.LCD_Clear(BLUE)
    text(35, 70, "SMART PRAYER", WHITE, BLUE, 24)
    text(70, 115, "BOOTING...", WHITE, BLUE, 16)
    print("Boot screen")


def show_wifi_connecting():
    if not lcd:
        return

    lcd.LCD_Clear(BLUE)
    text(35, 95, "WiFi Connecting", WHITE, BLUE, 16)
    print("WiFi connecting screen")


def show_wifi_connected():
    if not lcd:
        return

    lcd.LCD_Clear(GREEN)
    text(35, 95, "WiFi Connected", BLACK, GREEN, 16)
    print("WiFi connected screen")


def show_wifi_error():
    if not lcd:
        return

    lcd.LCD_Clear(RED)
    text(55, 95, "WiFi Error", WHITE, RED, 16)
    print("WiFi error screen")


def show_dashboard(prayer_times):

    if not lcd:
        return

    if not prayer_times:
        return

    next_name, next_time = get_next_prayer(prayer_times)

    lcd.Show_BMP_Pic("/background.bmp", 0, 0)

    # Header
    fill(0, 0, 320, 30, BLUE)
    text(8, 8, "SMART PRAYER SPEAKER", WHITE, BLUE)

    y = 40

    for prayer in PRAYERS:
        p_time = clean_time(prayer_times.get(prayer, "--:--"))

        if prayer == next_name:
            text(20, y + 5, "> " + prayer, YELLOW, BLACK)
            text(225, y + 5, p_time, YELLOW, BLACK)
        else:
            text(20, y + 5, prayer, WHITE, BLACK)
            text(225, y + 5, p_time, WHITE, BLACK)

        y += 30

    # Current clock
    now = time.localtime()

    clock = "{:02d}:{:02d}:{:02d}".format(
        now[3],
        now[4],
        now[5]
    )

    fill(0, 215, 320, 25, BLACK)
    text(110, 220, clock, CYAN, BLACK)