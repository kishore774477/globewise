import httpx


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Severe thunderstorm with hail",
}


async def search_locations(query: str, count: int = 5) -> list[dict]:
    params = {
        "name": query,
        "count": count,
        "language": "en",
        "format": "json",
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(GEOCODING_URL, params=params)
        response.raise_for_status()
        data = response.json()

    results = data.get("results", [])

    return [
        {
            "name": item.get("name"),
            "admin1": item.get("admin1"),
            "country": item.get("country"),
            "country_code": item.get("country_code"),
            "latitude": item.get("latitude"),
            "longitude": item.get("longitude"),
            "timezone": item.get("timezone"),
            "population": item.get("population"),
        }
        for item in results
    ]


async def get_weather(latitude: float, longitude: float) -> dict:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,precipitation",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(WEATHER_URL, params=params)
        response.raise_for_status()
        data = response.json()

    current = data.get("current", {})
    daily = data.get("daily", {})

    weather_code = current.get("weather_code")

    return {
        "temperature": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "condition": WEATHER_CODES.get(weather_code, "Unknown"),
        "weather_code": weather_code,
        "humidity": current.get("relative_humidity_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "precipitation": current.get("precipitation"),
        "daily": {
            "dates": daily.get("time", []),
            "max_temperature": daily.get("temperature_2m_max", []),
            "min_temperature": daily.get("temperature_2m_min", []),
            "rain_probability": daily.get("precipitation_probability_max", []),
        },
        "source": "Open-Meteo",
    }
