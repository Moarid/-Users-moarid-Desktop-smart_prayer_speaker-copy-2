from machine import Pin
import neopixel
import time

LED_PIN = 48
LED_COUNT = 24

np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

def clear():
    for i in range(LED_COUNT):
        np[i] = (0, 0, 0)
    np.write()

def set_color(r, g, b):
    for i in range(LED_COUNT):
        np[i] = (r, g, b)
    np.write()

def blink(r, g, b, times=3):
    for _ in range(times):
        set_color(r, g, b)
        time.sleep(0.25)
        clear()
        time.sleep(0.25)