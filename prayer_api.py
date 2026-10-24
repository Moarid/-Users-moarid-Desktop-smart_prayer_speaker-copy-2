try:
    import urequests as requests
except:
    import requests

try:
    import ujson as json
except:
    import json

import time

PRAYER_TIMES_FILE = "data/prayer_times.json"

def get_today_date():
    now = time.localtime()
    return "{:02}-{:02}-{}".format(now[2], now[1], now[0])

def save_prayer_times(prayer_data):
    with open(PRAYER_TIMES_FILE, "w") as file:
        json.dump(prayer_data, file)
    print("Prayer times saved:", PRAYER_TIMES_FILE)

def load_prayer_times():
    with open(PRAYER_TIMES_FILE, "r") as file:
        return json.load(file)

def get_prayer_times_by_location(latitude, longitude, method=2):
    date = get_today_date()
    url = (
        "https://api.aladhan.com/v1/timings/{}"
        "?latitude={}&longitude={}&method={}"
    ).format(date, latitude, longitude, method)

    print("Fetching prayer times...")
    print(url)

    response = requests.get(url)
    data = response.json()
    response.close()

    prayer_data = {
        "date": date,
        "timezone": data["data"]["meta"].get("timezone", ""),
        "timings": data["data"]["timings"]
    }

    save_prayer_times(prayer_data)
    return prayer_data
