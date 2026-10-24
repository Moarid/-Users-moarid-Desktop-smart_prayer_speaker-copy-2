try:
    import ujson as json
except:
    import json

CONFIG_FILE = "data/config.json"

DEFAULT_CONFIG = {
    "wifi_ssid": "",
    "wifi_password": "",
    "city": "Columbus",
    "country": "US",
    "prayer_method": 2,
    "timezone": "America/New_York",
    "led_brightness": 40,
    "audio_enabled": True,
    "morning_dua_enabled": True,
    "friday_kahf_enabled": True,
    "friday_kahf_time": "10:00",
    "led_pin": 5,
    "num_leds": 24,
    "audio_mode": "placeholder"
}

def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    except:
        config = DEFAULT_CONFIG.copy()
        save_config(config)

    changed = False
    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
            changed = True

    if changed:
        save_config(config)

    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)
    print("Config saved")
