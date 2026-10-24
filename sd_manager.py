from machine import Pin, SPI
import os
import sdcard
import time

SD_MOUNT_PATH = "/sd"
SOUNDS_PATH = "/sd/sounds"

def mount_sd():
    try:
        spi = SPI(
            1,
            baudrate=100000,
            polarity=0,
            phase=0,
            sck=Pin(12),
            mosi=Pin(11),
            miso=Pin(13)
        )

        cs = Pin(10, Pin.OUT, value=1)

        time.sleep(1)

        sd = sdcard.SDCard(spi, cs)

        try:
            os.umount(SD_MOUNT_PATH)
        except:
            pass

        os.mount(sd, SD_MOUNT_PATH)

        print("SD card mounted")
        print(os.listdir(SD_MOUNT_PATH))
        print(os.listdir(SOUNDS_PATH))

        return True

    except Exception as e:
        print("SD card mount failed:")
        print(e)
        return False