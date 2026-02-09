import requests
import os
from langchain.tools import tool
from dotenv import load_dotenv

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


@tool
def get_current_weather(city: str) -> str:
    """Get current weather for a city"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    res = requests.get(url).json()

    if "main" not in res:
        return "Weather data not available."

    return (
        f"Temperature: {res['main']['temp']}°C, "
        f"Condition: {res['weather'][0]['description']}"
    )


@tool
def get_weather_forecast(city: str) -> str:
    """Get weather forecast for a city"""
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    res = requests.get(url).json()

    if "list" not in res:
        return "Forecast not available."

    forecast = res["list"][:5]
    summary = []
    for item in forecast:
        summary.append(
            f"{item['dt_txt']}: {item['main']['temp']}°C, {item['weather'][0]['description']}"
        )

    return "\n".join(summary)


@tool
def search_flights(source: str, destination: str) -> str:
    """Mock flight search"""
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
