from machine import Pin
import neopixel
import time

# =========================================
# CONFIG
# =========================================

LED_PIN = 48       # Change to 14 if your LED DIN is connected to GPIO14
NUM_LEDS = 24

DEFAULT_BRIGHTNESS = 20
brightness = DEFAULT_BRIGHTNESS

pixels = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

# =========================================
# BASIC FUNCTIONS
# =========================================

def apply_brightness(color):
    r = int(color[0] * brightness / 255)
    g = int(color[1] * brightness / 255)
    b = int(color[2] * brightness / 255)
    return (r, g, b)


def grb(r, g, b):
    # WS2812 / NeoPixel usually uses GRB order
    return (g, r, b)


def set_brightness(value):
    global brightness
    brightness = max(1, min(255, value))


def clear():
    pixels.fill((0, 0, 0))
    pixels.write()


def off():
    clear()


def set_all(r, g, b):
    color = apply_brightness(grb(r, g, b))
    pixels.fill(color)
    pixels.write()


def set_pixel(index, r, g, b):
    if 0 <= index < NUM_LEDS:
        pixels[index] = apply_brightness(grb(r, g, b))
        pixels.write()

# =========================================
# SOLID COLORS
# =========================================

def red():
    set_all(255, 0, 0)


def green():
    set_all(0, 255, 0)


def blue():
    set_all(0, 0, 255)


def white():
    set_all(255, 255, 255)


def yellow():
    set_all(255, 150, 0)


def cyan():
    set_all(0, 255, 255)


def purple():
    set_all(180, 0, 255)

# =========================================
# ANIMATIONS
# =========================================

def startup_animation():
    clear()

    for i in range(NUM_LEDS):
        pixels[i] = apply_brightness(grb(0, 255, 0))
        pixels.write()
        time.sleep(0.03)

    time.sleep(0.3)

    for _ in range(2):
        blue()
        time.sleep(0.2)
        clear()
        time.sleep(0.2)


def loading(color=(0, 0, 255), delay=0.03):
    clear()

    r, g, b = color

    for i in range(NUM_LEDS):
        pixels[i] = apply_brightness(grb(r, g, b))
        pixels.write()
        time.sleep(delay)


def breathing_blue(cycles=3):
    global brightness

    old_brightness = brightness

    for _ in range(cycles):
        for i in range(1, 50):
            set_brightness(i)
            blue()
            time.sleep(0.02)

        for i in range(50, 1, -1):
            set_brightness(i)
            blue()
            time.sleep(0.02)

    brightness = old_brightness
    blue()


def wheel(pos):
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)

    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)

    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow_cycle(delay=0.01):
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            r, g, b = wheel(rc_index & 255)
            pixels[i] = apply_brightness(grb(r, g, b))

        pixels.write()
        time.sleep(delay)

# =========================================
# SYSTEM MODES
# =========================================

def setup_mode():
    # Trying to connect / setup WiFi = blue
    blue()


def idle_mode():
    # System running = white
    white()


def error_mode():
    # WiFi error = red
    red()


def prayer_mode():
    # Prayer call = green
    green()


def wifi_connected_mode():
    # WiFi connected / system OK = white
    white()


def wifi_failed_mode():
    # WiFi failed = red
    red()

# =========================================
# TEST
# =========================================

if __name__ == "__main__":
    startup_animation()

    while True:
        red()
        time.sleep(1)

        green()
        time.sleep(1)

        blue()
        time.sleep(1)

        white()
        time.sleep(1)

        yellow()
        time.sleep(1)

        cyan()
        time.sleep(1)

        purple()
        time.sleep(1)

        rainbow_cycle()