from app.providers.open_meteo import search_locations, get_weather
from app.providers.frankfurter import convert_currency
from app.providers.rest_countries import get_country_info
from app.providers.usgs_earthquake import get_nearby_earthquakes


def empty_weather() -> dict:
    return {
        "temperature": None,
        "feels_like": None,
        "condition": "Weather unavailable",
        "weather_code": None,
        "humidity": None,
        "wind_speed": None,
        "precipitation": None,
        "daily": {
            "dates": [],
            "max_temperature": [],
            "min_temperature": [],
            "rain_probability": [],
        },
        "source": "Unavailable",
    }


def empty_country_info(country: str = "Unknown") -> dict:
    return {
        "name": country or "Unknown",
        "capital": "Unknown",
        "currency_code": "USD",
        "currency_name": "US Dollar",
        "languages": [],
        "region": "Unknown",
        "subregion": "Unknown",
        "population": None,
        "timezones": [],
        "flag": "",
        "source": "Fallback",
    }


def empty_currency() -> dict:
    return {
        "amount": 1,
        "from_currency": "-",
        "to_currency": "-",
        "rate": None,
        "converted_amount": None,
        "source": "Unavailable",
    }


def get_risk_level(score: int) -> str:
    if score >= 75:
        return "Critical"
    if score >= 50:
        return "High"
    if score >= 25:
        return "Medium"
    return "Low"


def calculate_safety_score(weather: dict, earthquakes: list[dict]) -> tuple[int, list[str]]:
    score = 10
    reasons = []

    precipitation = weather.get("precipitation") or 0
    wind_speed = weather.get("wind_speed") or 0
    weather_code = weather.get("weather_code")

    if precipitation >= 10:
        score += 30
        reasons.append("Heavy precipitation is detected.")
    elif precipitation >= 2:
        score += 15
        reasons.append("Light to moderate precipitation is detected.")

    if wind_speed >= 50:
        score += 30
        reasons.append("Strong wind speed is detected.")
    elif wind_speed >= 30:
        score += 15
        reasons.append("Moderate wind speed is detected.")

    if weather_code in [95, 96, 99]:
        score += 25
        reasons.append("Thunderstorm conditions are possible.")

    if earthquakes:
        strongest = max([quake.get("magnitude") or 0 for quake in earthquakes])
        closest = min([quake.get("distance_km") or 99999 for quake in earthquakes])

        if strongest >= 6 and closest <= 500:
            score += 35
            reasons.append("A strong earthquake was detected within the nearby region.")
        elif strongest >= 4.5:
            score += 15
            reasons.append("Recent earthquake activity exists within the wider region.")

    score = min(score, 100)

    if not reasons:
        reasons.append("No major weather or earthquake risk detected right now.")

    return score, reasons


async def build_dashboard(city: str) -> dict:
    locations = await search_locations(city, count=1)

    if not locations:
        return {
            "location": {
                "name": city,
                "admin1": None,
                "country": "Unknown",
                "country_code": "XX",
                "latitude": None,
                "longitude": None,
                "timezone": None,
                "population": None,
            },
            "weather": empty_weather(),
            "country_info": empty_country_info(),
            "currency": empty_currency(),
            "safety": {
                "level": "Unknown",
                "score": 0,
                "reasons": ["Location was not found. Try a more specific city name."],
                "nearby_earthquakes": [],
            },
            "ai_tip": "Location was not found. Try searching with city and country, for example: Salem India or Salem United States.",
        }

    location = locations[0]

    weather = empty_weather()
    country_info = empty_country_info(location.get("country"))
    currency = empty_currency()
    earthquakes = []

    try:
        weather = await get_weather(
            latitude=location["latitude"],
            longitude=location["longitude"],
        )
    except Exception as exc:
        weather["condition"] = f"Weather unavailable: {str(exc)}"

    try:
        country_info = await get_country_info(location.get("country") or "Unknown")
    except Exception:
        country_info = empty_country_info(location.get("country"))

    try:
        local_currency = country_info.get("currency_code") or "USD"
        target_currency = "USD" if local_currency != "USD" else "INR"

        currency = await convert_currency(
            amount=1,
            from_currency=local_currency,
            to_currency=target_currency,
        )
    except Exception:
        currency = empty_currency()
        currency["from_currency"] = country_info.get("currency_code") or "-"
        currency["to_currency"] = "USD"

    try:
        earthquakes = await get_nearby_earthquakes(
            latitude=location["latitude"],
            longitude=location["longitude"],
            radius_km=800,
        )
    except Exception:
        earthquakes = []

    safety_score, risk_reasons = calculate_safety_score(weather, earthquakes)
    safety_level = get_risk_level(safety_score)

    temperature = weather.get("temperature")
    condition = weather.get("condition") or "unknown"

    ai_tip = (
        f"{location.get('name')} currently has a {safety_level.lower()} safety risk. "
        f"Weather condition is {condition}. "
    )

    if temperature is not None:
        ai_tip += f"Temperature is {temperature} deg C. "

    ai_tip += f"{risk_reasons[0]} Check local updates before travel and keep emergency contacts ready."

    return {
        "location": {
            "name": location.get("name") or city,
            "admin1": location.get("admin1"),
            "country": location.get("country") or "Unknown",
            "country_code": location.get("country_code") or "XX",
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "timezone": location.get("timezone"),
            "population": location.get("population"),
        },
        "weather": weather,
        "country_info": country_info,
        "currency": currency,
        "safety": {
            "level": safety_level,
            "score": safety_score,
            "reasons": risk_reasons,
            "nearby_earthquakes": earthquakes,
        },
        "ai_tip": ai_tip,
    }
