import time
import audio

class PrayerEngine:
    def __init__(self):
        self.prayer_times = {
            "Fajr": "05:12",
            "Dhuhr": "12:35",
            "Asr": "16:32",
            "Maghrib": "19:08",
            "Isha": "20:38",
        }

        self.triggered_today = {}
        self.last_day = None

    def current_time_text(self):
        now = time.localtime()
        return "{:02d}:{:02d}".format(now[3], now[4])

    def current_day_key(self):
        now = time.localtime()
        return "{}-{}-{}".format(now[0], now[1], now[2])

    def tick(self):
        day_key = self.current_day_key()

        if self.last_day != day_key:
            self.triggered_today = {}
            self.last_day = day_key

        now_text = self.current_time_text()

        for prayer_name, prayer_time in self.prayer_times.items():
            key = day_key + "_" + prayer_name

            if now_text == prayer_time and key not in self.triggered_today:
                self.triggered_today[key] = True
                self.call_prayer(prayer_name)

    def call_prayer(self, prayer_name):
        print("PRAYER TIME:", prayer_name)

        # Stop anything running
        audio.stop_all()

        # Play prayer sound
        audio.play_prayer(prayer_name)