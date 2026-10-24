from machine import Pin, I2C
from touch import FT6336
import time

# Initialize I2C
i2c = I2C(
    0,
    scl=Pin(15),
    sda=Pin(16),
    freq=400000
)

# Initialize touch
touch = FT6336(
    i2c,
    rst=18,
    width=320,
    height=240
)

# Match your LCD landscape rotation
touch.TP_Set_Rotation(1)

print("Touch Test Started")

while True:

    if touch.TP_Get_Touch():

        print(
            "X =",
            touch.tp_x[0],
            "Y =",
            touch.tp_y[0]
        )

        time.sleep_ms(200)