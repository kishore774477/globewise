from fastapi import APIRouter, Query
import math
import requests
from typing import Any, Dict, List, Optional

router = APIRouter()

OPEN_METEO_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
USGS_EARTHQUAKE_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

CITY_OVERRIDES = {
    "hosur": {
        "name": "Hosur",
        "admin1": "Tamil Nadu",
        "country": "India",
        "country_code": "IN",
        "latitude": 12.7409,
        "longitude": 77.8253,
        "timezone": "Asia/Kolkata",
    }
}


def safe_get(url: str, params: Optional[dict] = None, timeout: int = 12):
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def weather_code_to_text(code: Optional[int]) -> str:
    if code is None:
        return "Unknown"

    mapping = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    return mapping.get(code, "Unknown")


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(delta_lambda / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return radius * c


def resolve_city(city: str) -> Dict[str, Any]:
    city_key = city.strip().lower()

    if city_key in CITY_OVERRIDES:
        return CITY_OVERRIDES[city_key]

    data = safe_get(
        OPEN_METEO_GEOCODE_URL,
        params={
            "name": city,
            "count": 5,
            "language": "en",
            "format": "json",
        },
    )

    results = data.get("results", [])

    if not results:
        raise Exception(f"City not found: {city}")

    # Prefer India result if available, otherwise first result.
    selected = None

    for item in results:
        if item.get("country_code") == "IN":
            selected = item
            break

    if selected is None:
        selected = results[0]

    return {
        "name": selected.get("name", city),
        "admin1": selected.get("admin1", ""),
        "country": selected.get("country", ""),
        "country_code": selected.get("country_code", ""),
        "latitude": selected.get("latitude"),
        "longitude": selected.get("longitude"),
        "timezone": selected.get("timezone") or "auto",
    }


def get_weather(city_info: Dict[str, Any]) -> Dict[str, Any]:
    data = safe_get(
        OPEN_METEO_FORECAST_URL,
        params={
            "latitude": city_info["latitude"],
            "longitude": city_info["longitude"],
            "timezone": city_info.get("timezone") or "auto",
            "forecast_days": 7,
            "current": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "is_day",
                    "precipitation",
                    "weather_code",
                    "cloud_cover",
                    "wind_speed_10m",
                ]
            ),
            "daily": ",".join(
                [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_probability_max",
                ]
            ),
        },
    )

    current = data.get("current", {})
    daily = data.get("daily", {})

    weather_code = current.get("weather_code")

    return {
        "source": "Open-Meteo",
        "time": current.get("time"),
        "timezone": data.get("timezone"),
        "temperature_c": current.get("temperature_2m"),
        "feels_like_c": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"),
        "wind_kmh": current.get("wind_speed_10m"),
        "precipitation_mm": current.get("precipitation"),
        "cloud_cover": current.get("cloud_cover"),
        "weather_code": weather_code,
        "condition": weather_code_to_text(weather_code),
        "daily": {
            "time": daily.get("time", []),
            "max_temp_c": daily.get("temperature_2m_max", []),
            "min_temp_c": daily.get("temperature_2m_min", []),
            "weather_code": daily.get("weather_code", []),
            "precipitation_probability": daily.get(
                "precipitation_probability_max", []
            ),
        },
    }


def get_country_data(country_code: str) -> Dict[str, Any]:
    fallback = {
        "name": "India",
        "official_name": "Republic of India",
        "capital": "New Delhi",
        "region": "Asia",
        "subregion": "Southern Asia",
        "population": 1417173173,
        "currency_code": "INR",
        "currency": "Indian rupee ₹",
        "language": "Hindi, English",
        "flag": "🇮🇳",
        "timezone": "UTC+05:30",
    }

    if not country_code:
        return fallback

    # REST Countries v3.1 is deprecated, so use the bundled offline dataset.
    from app.providers.rest_countries import find_country, FALLBACK_COUNTRIES

    item = find_country(country_code)
    if item is None:
        return fallback

    currencies = item.get("currencies") or []
    currency_code = "INR"
    currency_text = "Indian rupee ₹"

    if currencies:
        currency_code = currencies[0].get("code") or currency_code
        currency_text = f"{currencies[0].get('name') or ''} {currencies[0].get('symbol') or ''}".strip()

    languages = item.get("languages") or []
    curated = FALLBACK_COUNTRIES.get(item["name"], {})

    return {
        "name": item.get("name") or "Unknown",
        "official_name": item.get("official_name") or "Unknown",
        "capital": item.get("capital") or "Unknown",
        "region": item.get("region") or "Unknown",
        "subregion": item.get("subregion") or "Unknown",
        "population": curated.get("population", 0),
        "currency_code": currency_code,
        "currency": currency_text,
        "language": ", ".join(languages) if languages else "Unknown",
        "flag": item.get("flag", ""),
        "timezone": ", ".join(curated.get("timezones", [])),
    }


def get_currency_rate(base: str = "INR", target: str = "USD") -> Dict[str, Any]:
    base = base.upper()
    target = target.upper()

    if base == target:
        return {
            "source": "Frankfurter",
            "base": base,
            "target": target,
            "rate": 1,
            "converted": 1,
            "date": None,
        }

    urls = [
        f"https://api.frankfurter.app/latest?from={base}&to={target}",
        f"https://api.frankfurter.dev/v1/latest?base={base}&symbols={target}",
    ]

    last_error = None

    for url in urls:
        try:
            data = safe_get(url)
            rate = data.get("rates", {}).get(target)

            if rate:
                return {
                    "source": "Frankfurter",
                    "base": base,
                    "target": target,
                    "rate": rate,
                    "converted": rate,
                    "date": data.get("date"),
                }

        except Exception as error:
            last_error = error

    return {
        "source": "Frankfurter fallback",
        "base": base,
        "target": target,
        "rate": 0,
        "converted": 0,
        "date": None,
        "error": str(last_error) if last_error else "Currency failed",
    }


def get_safety(city_info: Dict[str, Any], weather: Dict[str, Any]) -> Dict[str, Any]:
    lat = city_info["latitude"]
    lon = city_info["longitude"]

    earthquakes: List[Dict[str, Any]] = []

    try:
        data = safe_get(USGS_EARTHQUAKE_URL)
        features = data.get("features", [])

        for feature in features:
            props = feature.get("properties", {})
            geometry = feature.get("geometry", {})
            coordinates = geometry.get("coordinates", [])

            if len(coordinates) < 2:
                continue

            quake_lon = coordinates[0]
            quake_lat = coordinates[1]
            distance = haversine_km(lat, lon, quake_lat, quake_lon)

            if distance <= 500:
                earthquakes.append(
                    {
                        "place": props.get("place"),
                        "magnitude": props.get("mag"),
                        "distance_km": round(distance, 1),
                        "time": props.get("time"),
                    }
                )

    except Exception:
        earthquakes = []

    risk_score = 10
    reasons = []

    wind = weather.get("wind_kmh") or 0
    precipitation = weather.get("precipitation_mm") or 0
    weather_code = weather.get("weather_code")

    if wind >= 50:
        risk_score += 25
        reasons.append("Strong wind detected")

    if precipitation >= 10:
        risk_score += 20
        reasons.append("Heavy precipitation detected")

    if weather_code in [95, 96, 99]:
        risk_score += 30
        reasons.append("Thunderstorm condition detected")

    for quake in earthquakes:
        magnitude = quake.get("magnitude") or 0

        if magnitude >= 5:
            risk_score += 35
            reasons.append("Significant nearby earthquake detected")
            break

        if magnitude >= 3:
            risk_score += 15
            reasons.append("Minor nearby earthquake detected")
            break

    risk_score = min(risk_score, 100)

    if risk_score >= 70:
        level = "High"
    elif risk_score >= 40:
        level = "Medium"
    else:
        level = "Low"

    if not reasons:
        reasons.append("No major weather or earthquake risk detected right now")

    nearest_earthquake = None

    if earthquakes:
        nearest_earthquake = sorted(
            earthquakes, key=lambda item: item["distance_km"]
        )[0]

    return {
        "source": "Open-Meteo + USGS",
        "risk_score": risk_score,
        "level": level,
        "reasons": reasons,
        "nearby_earthquakes_count": len(earthquakes),
        "nearest_earthquake": nearest_earthquake,
    }


@router.get("/city/resolve")
def api_resolve_city(city: str = Query(default="Hosur")):
    return resolve_city(city)


@router.get("/analyze")
def api_analyze(
    city: str = Query(default="Hosur"),
    target_currency: str = Query(default="USD"),
):
    try:
        city_info = resolve_city(city)
    except Exception:
        city_info = CITY_OVERRIDES["hosur"]

    weather = get_weather(city_info)
    country = get_country_data(city_info.get("country_code", "IN"))
    currency = get_currency_rate(
        base=country.get("currency_code", "INR"),
        target=target_currency,
    )
    safety = get_safety(city_info, weather)

    return {
        "city": city_info,
        "weather": weather,
        "country": country,
        "currency": currency,
        "safety": safety,
    }


@router.get("/weather")
def api_weather(city: str = Query(default="Hosur")):
    city_info = resolve_city(city)
    return {
        "city": city_info,
        "weather": get_weather(city_info),
    }


@router.get("/country")
def api_country(city: str = Query(default="Hosur")):
    city_info = resolve_city(city)
    return {
        "city": city_info,
        "country": get_country_data(city_info.get("country_code", "IN")),
    }


@router.get("/currency")
def api_currency(
    city: str = Query(default="Hosur"),
    target_currency: str = Query(default="USD"),
):
    city_info = resolve_city(city)
    country = get_country_data(city_info.get("country_code", "IN"))

    return {
        "city": city_info,
        "country": country,
        "currency": get_currency_rate(
            base=country.get("currency_code", "INR"),
            target=target_currency,
        ),
    }


@router.get("/safety")
def api_safety(city: str = Query(default="Hosur")):
    city_info = resolve_city(city)
    weather = get_weather(city_info)

    return {
        "city": city_info,
        "weather": weather,
        "safety": get_safety(city_info, weather),
    }