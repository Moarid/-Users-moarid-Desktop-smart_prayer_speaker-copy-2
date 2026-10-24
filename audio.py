from machine import Pin, I2S
import time

def play_wav(path):
    print("Playing:", path)

    audio = I2S(
        0,
        sck=Pin(4),
        ws=Pin(5),
        sd=Pin(6),
        mode=I2S.TX,
        bits=16,
        format=I2S.MONO,
        rate=11025,
        ibuf=20000
    )

    try:
        with open(path, "rb") as f:
            f.read(44)

            while True:
                data = f.read(1024)

                if not data:
                    break

                audio.write(data)

            time.sleep(1)

    except Exception as e:
        print("Audio error:", e)

    audio.deinit()
    time.sleep(0.2)


# WiFi sounds
def play_wifi_connected():
    play_wav("/sounds/wifi_connected.wav")


def play_wifi_failed():
    play_wav("/sounds/wifi_failed.wav")

def play_time():
    play_wav("/time.wav")
    
# Prayer sounds
def play_fajr():
    play_wav("/sounds/test.wav")


def play_dhuhr():
    play_wav("/sounds/test.wav")


def play_asr():
    play_wav("/sounds/test.wav")


def play_maghrib():
    play_wav("/sounds/test.wav")


def play_isha():
    play_wav("/sounds/test.wav")
