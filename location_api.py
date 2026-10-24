try:
    import urequests as requests
except:
    import requests

def get_location_from_ip():
    url = "http://ip-api.com/json"
    print("Getting location from IP...")
    response = requests.get(url)
    data = response.json()
    response.close()

    if data.get("status") != "success":
        raise Exception("Location lookup failed")

    location = {
        "city": data.get("city"),
        "country": data.get("countryCode"),
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "timezone": data.get("timezone")
    }

    print("Detected location:", location)
    return location
