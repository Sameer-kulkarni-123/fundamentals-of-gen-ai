import requests
import os
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_lat_lon(city: str):
    """Convert city name to latitude and longitude"""
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city,
        "limit": 1,
        "appid": OPENWEATHER_API_KEY
    }

    res = requests.get(geo_url, params=params).json()

    if not res:
        return None, None

    return res[0]["lat"], res[0]["lon"]

@tool
def get_current_weather(city: str) -> str:
    """Get current weather for a city using OpenWeather One Call API"""
    lat, lon = get_lat_lon(city)

    if lat is None:
        return f"Could not find location for '{city}'."

    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,daily,alerts",
        "units": "metric",
        "appid": OPENWEATHER_API_KEY
    }

    res = requests.get(url, params=params).json()

    if "current" not in res:
        return f"Weather API error: {res}"

    weather = res["current"]

    return (
        f"Temperature: {weather['temp']}°C\n"
        f"Condition: {weather['weather'][0]['description']}"
    )




@tool
def get_weather_forecast(city: str) -> str:
    """Get daily forecast for a city using One Call API"""
    lat, lon = get_lat_lon(city)

    if lat is None:
        return "City not found."

    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,alerts",
        "units": "metric",
        "appid": OPENWEATHER_API_KEY
    }

    res = requests.get(url, params=params).json()

    if "daily" not in res:
        return "Forecast not available."

    forecast = res["daily"][:5]
    summary = []

    for day in forecast:
        summary.append(
            f"Temp: {day['temp']['day']}°C, {day['weather'][0]['description']}"
        )

    return "\n".join(summary)



@tool
def search_flights(route: str) -> str:
    """
    Search flights between two cities.
    Input should be in the format: 'source to destination'
    Example: 'Bangalore to Tokyo'
    """
    try:
        parts = route.lower().split(" to ")
        source = parts[0].title()
        destination = parts[1].title()
    except:
        return "Please provide input like: 'Bangalore to Tokyo'"

    return (
        f"Flights from {source} to {destination}:\n"
        "- Indigo: ₹55,000 (1 stop)\n"
        "- Emirates: ₹68,000 (1 stop)\n"
        "- ANA: ₹75,000 (direct)"
    )



@tool
def search_hotels(city: str) -> str:
    """Mock hotel search"""
    return (
        f"Hotels in {city}:\n"
        "- Budget: APA Hotel – ₹6,000/night\n"
        "- Mid-range: Hotel Mystays – ₹10,000/night\n"
        "- Luxury: Park Hyatt – ₹30,000/night"
    )


if __name__ == '__main__':
    print("API KEY:", OPENWEATHER_API_KEY)

