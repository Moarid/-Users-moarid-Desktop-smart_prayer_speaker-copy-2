try:
    import network
except:
    network = None

import socket
import time

try:
    import ujson as json
except:
    import json

AP_NAME = "SmartPrayerSpeaker_Setup"
AP_PASSWORD = "12345678"
CONFIG_FILE = "data/config.json"

def url_decode(text):
    text = text.replace("+", " ")
    result = ""
    i = 0
    while i < len(text):
        if text[i] == "%" and i + 2 < len(text):
            try:
                result += chr(int(text[i + 1:i + 3], 16))
                i += 3
            except:
                result += text[i]
                i += 1
        else:
            result += text[i]
            i += 1
    return result

def parse_form(body):
    data = {}
    for pair in body.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            data[url_decode(key.strip())] = url_decode(value.strip())
    return data

def scan_wifi_networks():
    wifi_names = []
    try:
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        time.sleep(2)
        print("Scanning WiFi networks...")
        networks = sta.scan()
        for net in networks:
            ssid = net[0].decode()
            if ssid and ssid not in wifi_names:
                wifi_names.append(ssid)
        print("Networks found:", wifi_names)
    except Exception as e:
        print("WiFi scan failed:", e)
    return wifi_names

def save_wifi_config(ssid, password):
    print("Saving WiFi...")
    config = {}
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    except Exception as e:
        print("Config read error:", e)

    config["wifi_ssid"] = ssid
    config["wifi_password"] = password

    if "city" not in config:
        config["city"] = "Columbus"
    if "country" not in config:
        config["country"] = "US"
    if "prayer_method" not in config:
        config["prayer_method"] = 2
    if "timezone" not in config:
        config["timezone"] = "America/New_York"
    if "friday_kahf_time" not in config:
        config["friday_kahf_time"] = "10:00"
    if "led_brightness" not in config:
        config["led_brightness"] = 40
    if "led_pin" not in config:
        config["led_pin"] = 5
    if "num_leds" not in config:
        config["num_leds"] = 24

    print("SSID:", ssid)
    print("PASSWORD:", password)

    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

    print("WiFi config saved successfully")
    with open(CONFIG_FILE, "r") as file:
        print("VERIFY:", file.read())

def html_page(networks=None, message="", error=""):
    if networks is None:
        networks = []
    options = ""
    for ssid in networks:
        options += '<option value="{}">{}</option>'.format(ssid, ssid)

    html = """HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
<title>Smart Prayer Speaker Setup</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {font-family:Arial;background:#f4f4f4;padding:20px;}
.card {background:white;max-width:420px;margin:auto;padding:25px;border-radius:16px;box-shadow:0 4px 16px rgba(0,0,0,0.15);}
h2 {text-align:center;}
select,input {width:100%;padding:14px;margin-top:10px;margin-bottom:20px;border-radius:10px;border:1px solid #ccc;font-size:16px;}
button {width:100%;padding:14px;border:none;border-radius:10px;background:#0a7c4a;color:white;font-size:18px;}
.msg {color:green;font-weight:bold;text-align:center;}
.error {color:red;font-weight:bold;text-align:center;}
</style>
</head>
<body>
<div class="card">
<h2>Smart Prayer Speaker</h2>
<p>Select your home Wi-Fi and enter password.</p>
<p class="msg">__MESSAGE__</p>
<p class="error">__ERROR__</p>
<form method="POST">
<label>Available Wi-Fi Networks</label>
<select name="ssid" required>
__OPTIONS__
</select>
<label>Wi-Fi Password</label>
<input name="password" type="password" placeholder="Enter Wi-Fi password" required>
<button type="submit">Connect Speaker</button>
</form>
<form method="GET">
<button style="margin-top:15px;background:#555;">Refresh Wi-Fi List</button>
</form>
</div>
</body>
</html>
"""
    html = html.replace("__OPTIONS__", options)
    html = html.replace("__MESSAGE__", message)
    html = html.replace("__ERROR__", error)
    return html

def success_page(message):
    return """HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="font-family:Arial;background:#f4f4f4;padding:20px;">
<div style="background:white;max-width:420px;margin:auto;padding:25px;border-radius:16px;text-align:center;">
<h2>Success</h2>
<p>""" + message + """</p>
</div>
</body>
</html>
"""

def start_setup_portal():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=AP_NAME, password=AP_PASSWORD)

    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    host = "0.0.0.0"
    port = 80

    print("Setup WiFi created")
    print("SSID:", AP_NAME)
    print("Password:", AP_PASSWORD)
    print("Open: http://192.168.4.1")

    addr = socket.getaddrinfo(host, port)[0][-1]
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    server.listen(1)

    while True:
        client, addr = server.accept()
        try:
            request = client.recv(8192)
            request = request.decode("utf-8", "ignore")
            print(request)

            if "POST" in request:
                if "\r\n\r\n" in request:
                    body = request.split("\r\n\r\n", 1)[1]
                    print("BODY:", body)
                else:
                    body = ""

                form = parse_form(body)
                print("FORM:", form)

                ssid = form.get("ssid", "").strip()
                password = form.get("password", "").strip()
                password = password.replace("\n", "")
                password = password.replace("\r", "")
                password = password.replace("\t", "")

                save_wifi_config(ssid, password)

                response = success_page("WiFi saved. Restarting device...")
                client.sendall(response.encode())
                client.close()

                time.sleep(2)
                import machine
                machine.reset()
                return

            else:
                networks = scan_wifi_networks()
                response = html_page(networks)
                client.sendall(response.encode())

        except Exception as e:
            print("Setup portal error:", e)

        finally:
            try:
                client.close()
            except:
                pass
