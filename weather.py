import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

WEATHERAPI_KEY = os.environ.get("WEATHERAPI_KEY", "")


def get_weather_data(lat, lon):
    """Fetch weather data from WeatherAPI.com"""
    
    # Skip if no API key configured
    if not WEATHERAPI_KEY or WEATHERAPI_KEY == "your_api_key_here":
        logger.warning("WeatherAPI key not configured - using defaults")
        return None
    
    try:
        url = "http://api.weatherapi.com/v1/current.json"
        params = {
            "key": WEATHERAPI_KEY,
            "q": f"{lat},{lon}",
            "aqi": "yes"  # Include air quality data
        }

        response = requests.get(url, params=params, timeout=5)
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
    except requests.exceptions.Timeout:
        logger.error("Weather API timeout")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Weather API request error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Weather API error: {str(e)}")
        return None