import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
import pytz

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY") or "a33f002e15815cd014e242b417f9b7e1"
DEBUG = False

def debug_log(msg):
    if DEBUG:
        print(msg)

# 📍 Get coordinates for a city
def get_coordinates(city):
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    res = requests.get(url)
    if res.status_code == 200 and res.json():
        data = res.json()[0]
        return data['lat'], data['lon']
    return None, None

# 🌦️ Get current weather + AQI + gas ratios
def get_weather(city):
    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        return None

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    weather_res = requests.get(weather_url)
    if weather_res.status_code != 200:
        return None

    data = weather_res.json()
    condition = data['weather'][0]['description'].title()
    temp = data['main']['temp']
    humidity = data['main'].get('humidity', '--')
    wind_kph = round(data['wind']['speed'] * 3.6, 1)
    wind_dir = "--"
    uv = 0

    # 🌅 Convert UTC to IST
    tz_ist = pytz.timezone('Asia/Kolkata')
    sunrise_ts = data['sys'].get('sunrise')
    sunset_ts = data['sys'].get('sunset')
    sunrise = datetime.utcfromtimestamp(sunrise_ts).replace(tzinfo=pytz.utc).astimezone(tz_ist).strftime('%I:%M %p') if sunrise_ts else "--"
    sunset = datetime.utcfromtimestamp(sunset_ts).replace(tzinfo=pytz.utc).astimezone(tz_ist).strftime('%I:%M %p') if sunset_ts else "--"

    # 🌫️ AQI and gas data
    aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    aqi_res = requests.get(aqi_url)

    if aqi_res.status_code == 200:
        aqi_data = aqi_res.json()
        aqi = aqi_data['list'][0]['main']['aqi']
        components = aqi_data['list'][0]['components']
    else:
        aqi = None
        components = {}

    return {
        'weather': condition,
        'temp': temp,
        'humidity': humidity,
        'wind_kph': wind_kph,
        'wind_dir': wind_dir,
        'sunrise': sunrise,
        'sunset': sunset,
        'uv': uv,
        'aqi': aqi,
        'components': components,
        'lat': lat,
        'lon': lon
    }

# 📅 5-Day Forecast
def get_forecast(city):
    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        return [], []

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    res = requests.get(forecast_url)
    if res.status_code != 200:
        return [], []

    data = res.json()
    entries = data['list'][::8]
    dates = [entry['dt_txt'].split(' ')[0] for entry in entries]
    temps = [entry['main']['temp'] for entry in entries]
    return dates, temps

# ⏰ Hourly Forecast
def get_hourly_forecast(city):
    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        return []

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    res = requests.get(url)
    if res.status_code != 200:
        return []

    data = res.json()
    hourly_data = []
    for entry in data["list"][:8]:
        time = entry["dt_txt"]
        temp = entry["main"]["temp"]
        condition = entry["weather"][0]["description"].title()
        hourly_data.append({
            "time": time,
            "temp": temp,
            "desc": condition
        })

    return hourly_data

# 📍 Nearby Weather with Temperature
def get_nearby_weather(lat, lon, radius_km=200):
    CITIES_CSV_PATH = "data/worldcities.csv"
    try:
        cities_df = pd.read_csv(CITIES_CSV_PATH)
        cities_df = cities_df[cities_df['country'] == 'India']
    except Exception as e:
        return []

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    candidates = []
    for _, row in cities_df.iterrows():
        dist = haversine(lat, lon, row['lat'], row['lng'])
        if 40 < dist <= radius_km:  # ✅ Skip cities too close (< 40 km)
            try:
                weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={row['lat']}&lon={row['lng']}&units=metric&appid={API_KEY}"
                res = requests.get(weather_url)
                temp = res.json()['main']['temp'] if res.status_code == 200 else None
            except Exception:
                temp = None

            candidates.append({
                'city': row['city'],
                'lat': row['lat'],
                'lon': row['lng'],
                'distance_km': round(dist, 1),
                'temp': temp
            })

    # ✅ Sort by distance and pick top 6 spaced-out cities
    selected = []
    used_coords = []

    for entry in sorted(candidates, key=lambda x: x['distance_km']):
        too_close = any(
            haversine(entry['lat'], entry['lon'], used_lat, used_lon) < 30
            for used_lat, used_lon in used_coords
        )
        if not too_close:
            selected.append(entry)
            used_coords.append((entry['lat'], entry['lon']))
        if len(selected) >= 6:
            break

    return selected
