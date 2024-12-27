import os
import requests
from flask import current_app

WEATHERAPI_KEY = os.environ.get("WEATHERAPI_KEY", "YOUR_API_KEY")

def get_weather_data(lat, lon):
    """Fetch weather data from WeatherAPI.com"""
    try:
        url = "http://api.weatherapi.com/v1/current.json"
        params = {
            "key": WEATHERAPI_KEY,
            "q": f"{lat},{lon}",
            "aqi": "yes"  # Include air quality data
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        return {
            "temperature": round(data["current"]["temp_c"]),
            "humidity": data["current"]["humidity"],
            "description": data["current"]["condition"]["text"],
            "uv_index": data["current"]["uv"],
            "location": {
                "city": data["location"]["name"],
                "region": data["location"]["region"],
                "country": data["location"]["country"]
            }
        }
    except Exception as e:
        current_app.logger.error(f"Weather API error: {str(e)}")
        return None