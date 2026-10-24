from Font_12x24_EN import Font_12x24_EN
from Font_8x16_EN import Font_8x16_EN

BLACK=0x0000
WHITE=0xFFFF
YELLOW=0xFFE0
RED=0xF800

class SettingsPage:

    def draw(self,lcd):

        lcd.LCD_Clear(BLACK)

        lcd.Show_String(95,10,"Settings",Font_12x24_EN,WHITE,BLACK)

        lcd.Fill_Round_Rect(20,60,120,60,5,YELLOW)
        lcd.Fill_Round_Rect(180,60,120,60,5,YELLOW)
        lcd.Fill_Round_Rect(20,140,120,60,5,YELLOW)
        lcd.Fill_Round_Rect(180,140,120,60,5,YELLOW)

        lcd.Show_String(25,85,"Connectivity",Font_8x16_EN,BLACK,YELLOW)
        lcd.Show_String(215,85,"Display",Font_8x16_EN,BLACK,YELLOW)
        lcd.Show_String(30,165,"Prayer Setup",Font_8x16_EN,BLACK,YELLOW)
        lcd.Show_String(215,165,"System",Font_8x16_EN,BLACK,YELLOW)

        lcd.Fill_Round_Rect(10,10,70,35,5,RED)
        lcd.Show_String(22,20,"Back",Font_8x16_EN,WHITE,RED)

    def handle_touch(self,x,y):
        print("Prayer touch:", x, y)
        
        if 170 <= x <= 215 and 170 <= y <= 215:
            print("Back pressed")
            return "back"

        return None