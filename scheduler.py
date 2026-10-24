import time
from audio import (
    play_fajr,
    play_dhuhr,
    play_asr,
    play_maghrib,
    play_isha
)
import led_controller

IMPORTANT_PRAYERS = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

triggered_today = {}


def clean_time(value):
    return value[:5]


def time_to_minutes(value):
    hour, minute = value.split(":")
    return int(hour) * 60 + int(minute)


def current_minutes():
    now = time.localtime()
    return now[3] * 60 + now[4]


def play_prayer_sound(prayer):
    if prayer == "Fajr":
        play_fajr()
    elif prayer == "Dhuhr":
        play_dhuhr()
    elif prayer == "Asr":
        play_asr()
    elif prayer == "Maghrib":
        play_maghrib()
    elif prayer == "Isha":
        play_isha()


def check_prayer_times(prayer_times):
    now_minutes = current_minutes()

    for prayer in IMPORTANT_PRAYERS:
        if prayer not in prayer_times:
            continue

        prayer_time = clean_time(prayer_times[prayer])
        prayer_minutes = time_to_minutes(prayer_time)

        reminder_time = prayer_minutes - 15

        if now_minutes == reminder_time:
            reminder_key = prayer + "_reminder_" + prayer_time

            if triggered_today.get(reminder_key) != reminder_key:
                print("15 minutes before", prayer)
                led_controller.warning_mode()
                triggered_today[reminder_key] = reminder_key

        if now_minutes == prayer_minutes:
            prayer_key = prayer + "_adhan_" + prayer_time

            if triggered_today.get(prayer_key) != prayer_key:
                print("{} time: {}".format(prayer, prayer_time))

                led_controller.prayer_mode()
                play_prayer_sound(prayer)

                time.sleep(180)

                led_controller.idle_mode()
                triggered_today[prayer_key] = prayer_key


def print_next_schedule(prayer_times):
    print("\\nToday's Prayer Schedule")

    for prayer in IMPORTANT_PRAYERS:
        if prayer in prayer_times:
            print(prayer, clean_time(prayer_times[prayer]))