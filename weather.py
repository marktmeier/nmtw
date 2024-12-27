import os
import requests
from flask import current_app

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_API_KEY")

def get_weather_data(lat, lon):
    """Fetch weather data from OpenWeather API"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "temperature": round(data["main"]["temp"]),
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "uv_index": get_uv_index(lat, lon)
        }
    except Exception as e:
        current_app.logger.error(f"Weather API error: {str(e)}")
        return None

def get_uv_index(lat, lon):
    """Fetch UV index data from OpenWeather API"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/uvi"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return round(data["value"], 1)
    except:
        return None
