from Font_12x24_EN import Font_12x24_EN
from Font_8x16_EN import Font_8x16_EN

BLACK=0x0000
WHITE=0xFFFF
CYAN=0x07FF
RED=0xF800

class AudioPage:

    def draw(self,lcd):

        lcd.LCD_Clear(BLACK)

        lcd.Show_String(110,10,"Audio",Font_12x24_EN,WHITE,BLACK)

        lcd.Fill_Round_Rect(20,60,120,60,5,CYAN)
        lcd.Fill_Round_Rect(180,60,120,60,5,CYAN)
        lcd.Fill_Round_Rect(20,140,120,60,5,CYAN)
        lcd.Fill_Round_Rect(180,140,120,60,5,CYAN)

        lcd.Show_String(35,85,"Nasheed",Font_8x16_EN,BLACK,CYAN)
        lcd.Show_String(205,85,"Lectures",Font_8x16_EN,BLACK,CYAN)
        lcd.Show_String(25,165,"Quran Radio",Font_8x16_EN,BLACK,CYAN)
        lcd.Show_String(195,165,"Local Files",Font_8x16_EN,BLACK,CYAN)

        lcd.Fill_Round_Rect(10,10,70,35,5,RED)
        lcd.Show_String(22,20,"Back",Font_8x16_EN,WHITE,RED)

    def handle_touch(self,x,y):
        print("Prayer touch:", x, y)
        
        if 170 <= x <= 215 and 170 <= y <= 215:
            print("Back pressed")
            return "back"

        return None