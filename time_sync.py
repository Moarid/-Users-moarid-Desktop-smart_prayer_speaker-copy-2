try:
    import ntptime
except:
    ntptime = None

import time
import machine

UTC_OFFSET_SECONDS = -4 * 60 * 60  # Ohio EDT

def sync_time():
    try:
        print("Syncing time with NTP...")
        ntptime.settime()

        utc = time.time()
        local = utc + UTC_OFFSET_SECONDS

        tm = time.localtime(local)

        rtc = machine.RTC()
        rtc.datetime((
            tm[0],
            tm[1],
            tm[2],
            tm[6] + 1,
            tm[3],
            tm[4],
            tm[5],
            0
        ))

        print("Local time synced:", time.localtime())
        return True

    except Exception as e:
        print("NTP sync failed:", e)
        return False