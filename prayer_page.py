from Font_12x24_EN import Font_12x24_EN
from Font_8x16_EN import Font_8x16_EN

BLACK = 0x0000
WHITE = 0xFFFF
GREEN = 0x07E0
BLUE = 0x001F
RED = 0xF800
GRAY = 0x8410


class PrayerPage:

    def __init__(self):

        self.buttons = [

            {
                "label": "Back",
                "target": "back",
                "x": 10,
                "y": 10,
                "w": 70,
                "h": 35,
                "color": RED
            }

        ]

    def draw(self, lcd):

        lcd.LCD_Clear(BLACK)

        lcd.Show_String(
            110,
            10,
            "Prayer",
            Font_12x24_EN,
            WHITE,
            BLACK
        )

        lcd.Fill_Round_Rect(10, 55, 300, 165, 8, GRAY)

        lcd.Show_String(
            20,
            70,
            "Fajr      05:12",
            Font_8x16_EN,
            WHITE,
            GRAY
        )

        lcd.Show_String(
            20,
            95,
            "Dhuhr     01:24",
            Font_8x16_EN,
            WHITE,
            GRAY
        )

        lcd.Show_String(
            20,
            120,
            "Asr       05:05",
            Font_8x16_EN,
            WHITE,
            GRAY
        )

        lcd.Show_String(
            20,
            145,
            "Maghrib   08:41",
            Font_8x16_EN,
            WHITE,
            GRAY
        )

        lcd.Show_String(
            20,
            170,
            "Isha      10:08",
            Font_8x16_EN,
            WHITE,
            GRAY
        )

        lcd.Fill_Round_Rect(10, 10, 70, 35, 5, RED)

        lcd.Show_String(
            22,
            20,
            "Back",
            Font_8x16_EN,
            WHITE,
            RED
        )

    def handle_touch(self, x, y):

        print("Prayer touch:", x, y)
        
        if 170 <= x <= 215 and 170 <= y <= 215:
            print("Back pressed")
            return "back"

        return None