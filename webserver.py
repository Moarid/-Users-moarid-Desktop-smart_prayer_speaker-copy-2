import socket
from prayer_api import load_prayer_times
from config import load_config, save_config

def parse_request_path(request):
    first_line = request.split("\r\n")[0]
    parts = first_line.split(" ")
    if len(parts) >= 2:
        return parts[1]
    return "/"

def url_decode(text):
    text = text.replace("+", " ")
    parts = text.split("%")
    result = parts[0]
    for item in parts[1:]:
        try:
            result += chr(int(item[:2], 16)) + item[2:]
        except:
            result += "%" + item
    return result

def parse_query(path):
    data = {}
    if "?" not in path:
        return data
    query = path.split("?", 1)[1]
    for pair in query.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            data[url_decode(key)] = url_decode(value)
    return data

def dashboard_page(message=""):
    config = load_config()
    try:
        prayer_data = load_prayer_times()
        timings = prayer_data.get("timings", {})
        rows = ""
        for name in ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]:
            if name in timings:
                rows += "<tr><td>{}</td><td>{}</td></tr>".format(name, timings[name])
    except:
        rows = "<tr><td colspan='2'>No prayer times saved yet</td></tr>"

    friday_time = config.get("friday_kahf_time", "10:00")

    html = """HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head>
<title>Smart Prayer Speaker</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {font-family:Arial;background:#f4f4f4;padding:20px;}
.card {background:white;max-width:520px;margin:auto;padding:25px;border-radius:16px;}
table {width:100%;border-collapse:collapse;}
td {padding:10px;border-bottom:1px solid #ddd;}
input,button {width:100%;padding:12px;margin:8px 0;border-radius:10px;border:1px solid #ccc;}
button {background:#0a7c4a;color:white;border:none;font-size:16px;}
.msg {color:green;font-weight:bold;text-align:center;}
</style>
</head>
<body>
<div class="card">
<h2>Smart Prayer Speaker</h2>
<p class="msg">__MESSAGE__</p>
<h3>Today's Prayer Times</h3>
<table>__ROWS__</table>
<h3>Friday Al-Kahf</h3>
<p>Current play time: <strong>__FRIDAY_TIME__</strong></p>
<form method="GET" action="/settings">
<label>Friday Al-Kahf Time</label>
<input name="friday_kahf_time" type="time" value="__FRIDAY_TIME__">
<button type="submit">Save Friday Time</button>
</form>
</div>
</body>
</html>
"""
    html = html.replace("__MESSAGE__", message)
    html = html.replace("__ROWS__", rows)
    html = html.replace("__FRIDAY_TIME__", friday_time)
    return html

def start_webserver(port=80):
    host = "0.0.0.0"
    addr = socket.getaddrinfo(host, port)[0][-1]
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    server.listen(1)
    print("Web server running on port", port)

    while True:
        client, addr = server.accept()
        try:
            request = client.recv(4096).decode()
            path = parse_request_path(request)

            if path.startswith("/settings"):
                params = parse_query(path)
                config = load_config()
                if "friday_kahf_time" in params:
                    config["friday_kahf_time"] = params["friday_kahf_time"]
                    save_config(config)
                    response = dashboard_page("Friday Al-Kahf time saved.")
                else:
                    response = dashboard_page()
            else:
                response = dashboard_page()

            client.sendall(response.encode())

        except Exception as e:
            print("Dashboard error:", e)
            response = "HTTP/1.1 200 OK\\r\\nContent-Type: text/html\\r\\n\\r\\n<h2>Error</h2>"
            client.sendall(response.encode())
        finally:
            client.close()
