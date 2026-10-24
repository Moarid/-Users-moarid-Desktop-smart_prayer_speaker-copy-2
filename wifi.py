try:
    import network
except:
    network = None

import time

def connect_wifi(ssid, password, timeout_seconds=25):
    if not ssid:
        print("No WiFi SSID saved")
        return None

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print("Already connected:", wlan.ifconfig())
        return wlan

    print("Connecting to WiFi:", ssid)
    wlan.connect(ssid, password)

    timeout = timeout_seconds
    while not wlan.isconnected() and timeout > 0:
        print("Connecting...")
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("WiFi connected:", wlan.ifconfig())
        return wlan

    print("WiFi connection failed")
    return None
