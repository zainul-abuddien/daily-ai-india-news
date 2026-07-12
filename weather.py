from __future__ import annotations

import requests


def get_weather() -> dict:
    """
    Get current weather for Gangavathi, Karnataka.
    Uses Open-Meteo free API.
    """

    latitude = 15.433
    longitude = 76.533

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,weather_code"
        "&timezone=Asia/Kolkata"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        current = data["current"]

        return {
            "temperature": f"{current['temperature_2m']}°C",
            "humidity": f"{current['relative_humidity_2m']}%",
            "condition": weather_description(
                current["weather_code"]
            ),
        }

    except Exception as e:
        return {
            "temperature": "Unavailable",
            "humidity": "Unavailable",
            "condition": str(e),
        }


def weather_description(code: int) -> str:
    """
    Convert Open-Meteo weather codes to readable text.
    """

    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Cloudy",
        45: "Fog",
        48: "Fog",
        51: "Light drizzle",
        61: "Rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Snow",
        80: "Rain showers",
        95: "Thunderstorm",
    }

    return descriptions.get(code, "Mixed conditions")