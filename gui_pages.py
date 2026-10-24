PAGES = {
    "home": {
        "title": "Home",
        "back": None,
        "buttons": [
            ("Prayer", "prayer"),
            ("Quran", "quran"),
            ("Audio", "audio"),
            ("Settings", "settings"),
        ],
    },

    "prayer": {
        "title": "Prayer",
        "back": "home",
        "buttons": [
            ("Fajr", None),
            ("Dhuhr", None),
            ("Asr", None),
            ("Maghrib", None),
            ("Isha", None),
            ("Hijri Date", None),
            ("Time / Date", None),
        ],
    },

    "quran": {
        "title": "Quran",
        "back": "home",
        "buttons": [
            ("Surahs", "surahs"),
            ("Dua", "dua"),
            ("Tasbeeh", "tasbeeh"),
            ("Ruqyah", "ruqyah"),
        ],
    },

    "surahs": {
        "title": "Surahs 1/29",
        "back": "quran",
        "buttons": [
            ("Al-Fatiha", None),
            ("Al-Baqarah", None),
            ("Aal-Imran", None),
            ("An-Nisa", None),
        ],
    },

    "dua": {
        "title": "Dua 1/3",
        "back": "quran",
        "buttons": [
            ("Morning Dua", None),
            ("Evening Dua", None),
            ("Before Sleep", None),
            ("Travel Dua", None),
        ],
    },

    "tasbeeh": {
        "title": "Tasbeeh",
        "back": "quran",
        "buttons": [
            ("SubhanAllah 33", None),
            ("Alhamdulillah 33", None),
            ("Allahu Akbar 34", None),
            ("Reset Count", None),
        ],
    },

    "ruqyah": {
        "title": "Ruqyah 1/2",
        "back": "quran",
        "buttons": [
            ("Full Ruqyah", None),
            ("Ayat Al-Kursi", None),
            ("Last 2 Verses", None),
            ("Al-Ikhlas x3", None),
        ],
    },

    "audio": {
        "title": "Audio",
        "back": "home",
        "buttons": [
            ("Volume", None),
            ("Prayer Voice", None),
            ("Quran Reciter", None),
            ("Test Audio", None),
        ],
    },

    "settings": {
        "title": "Settings",
        "back": "home",
        "buttons": [
            ("Connectivity", "connectivity"),
            ("Display", "display"),
            ("Prayer Setup", "prayer_setup"),
            ("System", "system"),
        ],
    },

    "connectivity": {
        "title": "Connectivity",
        "back": "settings",
        "buttons": [
            ("WiFi", "wifi"),
            ("Bluetooth", "bluetooth"),
            ("Network Status", None),
            ("Update Check", None),
        ],
    },

    "wifi": {
        "title": "WiFi",
        "back": "connectivity",
        "buttons": [
            ("Scan Networks", None),
            ("Saved Networks", None),
            ("Forget WiFi", None),
            ("WiFi Status", None),
        ],
    },

    "bluetooth": {
        "title": "Bluetooth",
        "back": "connectivity",
        "buttons": [
            ("Scan Speakers", None),
            ("Saved Speakers", None),
            ("Connect", None),
            ("Test Speaker", None),
        ],
    },

    "display": {
        "title": "Display",
        "back": "settings",
        "buttons": [
            ("Brightness", None),
            ("Theme", None),
            ("Screen Timeout", None),
            ("Touch Calibrate", None),
        ],
    },

    "prayer_setup": {
        "title": "Prayer Setup",
        "back": "settings",
        "buttons": [
            ("Method", None),
            ("Reminder", None),
            ("Time Format", None),
            ("Friday Settings", None),
        ],
    },

    "system": {
        "title": "System",
        "back": "settings",
        "buttons": [
            ("System Info", None),
            ("Storage", None),
            ("Logs", None),
            ("Restart", None),
        ],
    },
}