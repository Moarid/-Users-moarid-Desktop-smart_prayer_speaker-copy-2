from Font_12x24_EN import Font_12x24_EN
from Font_8x16_EN import Font_8x16_EN

BLACK = 0x0000
WHITE = 0xFFFF
GREEN = 0x07E0
BLUE = 0x001F
YELLOW = 0xFFE0
CYAN = 0x07FF

class HomePage:

    def __init__(self):
        self.title = "Home"

        self.buttons = [
            {"label": "Prayer",   "target": "prayer",   "x": 10,  "y": 45,  "w": 145, "h": 80, "color": GREEN},
            {"label": "Quran",    "target": "quran",    "x": 165, "y": 45,  "w": 145, "h": 80, "color": BLUE},
            {"label": "Audio",    "target": "audio",    "x": 10,  "y": 140, "w": 145, "h": 80, "color": CYAN},
            {"label": "Settings", "target": "settings", "x": 165, "y": 140, "w": 145, "h": 80, "color": YELLOW},
        ]

    def draw(self, lcd):
        lcd.LCD_Clear(BLACK)

        lcd.Show_String(
            70,
            10,
            "Smart Prayer",
            Font_12x24_EN,
            WHITE,
            BLACK
        )

        for button in self.buttons:
            x = button["x"]
            y = button["y"]
            w = button["w"]
            h = button["h"]
            label = button["label"]
            color = button["color"]

            lcd.Fill_Round_Rect(x, y, w, h, 8, color)
            lcd.Draw_Round_Rect(x, y, w, h, 8, WHITE)

            text_width = len(label) * 8
            text_x = x + int((w - text_width) / 2)
            text_y = y + int((h - 16) / 2)

            lcd.Show_String(
                text_x,
                text_y,
                label,
                Font_8x16_EN,
                BLACK,
                color
            )

    def handle_touch(self, x, y):

        print("Raw touch:", x, y)

        # Prayer
        if 120 <= x <= 180 and 120 <= y <= 180:
            print("Pressed: Prayer")
            return "prayer"

        # Quran
        if 0 <= x <= 60 and 120 <= y <= 180:
            print("Pressed: Quran")
            return "quran"

        # Audio
        if 120 <= x <= 190 and 40 <= y <= 90:
            print("Pressed: Audio")
            return "audio"

        # Settings
        if -10 <= x <= 50 and 40 <= y <= 90:
            print("Pressed: Settings")
            return "settings"

        return None
