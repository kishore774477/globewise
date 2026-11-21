"""Country information provider.

The public REST Countries v3.1 API was deprecated and v5 requires an API key,
so GlobeWise ships an offline dataset (app/data/countries.json, derived from
the open mledoze/countries project) and looks countries up locally.
"""

import json
from functools import lru_cache
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "countries.json"

FALLBACK_COUNTRIES = {
    "India": {
        "name": "India",
        "capital": "New Delhi",
        "currency_code": "INR",
        "currency_name": "Indian rupee",
        "languages": ["Hindi", "English", "Tamil"],
        "region": "Asia",
        "subregion": "Southern Asia",
        "population": 1428627663,
        "timezones": ["UTC+05:30"],
        "flag": "🇮🇳",
        "source": "Fallback Database",
    },
    "United Arab Emirates": {
        "name": "United Arab Emirates",
        "capital": "Abu Dhabi",
        "currency_code": "AED",
        "currency_name": "United Arab Emirates dirham",
        "languages": ["Arabic", "English"],
        "region": "Asia",
        "subregion": "Western Asia",
        "population": 9890400,
        "timezones": ["UTC+04:00"],
        "flag": "🇦🇪",
        "source": "Fallback Database",
    },
    "Japan": {
        "name": "Japan",
        "capital": "Tokyo",
        "currency_code": "JPY",
        "currency_name": "Japanese yen",
        "languages": ["Japanese"],
        "region": "Asia",
        "subregion": "Eastern Asia",
        "population": 125800000,
        "timezones": ["UTC+09:00"],
        "flag": "🇯🇵",
        "source": "Fallback Database",
    },
    "United States": {
        "name": "United States",
        "capital": "Washington, D.C.",
        "currency_code": "USD",
        "currency_name": "United States dollar",
        "languages": ["English"],
        "region": "Americas",
        "subregion": "North America",
        "population": 331900000,
        "timezones": ["UTC-05:00", "UTC-06:00", "UTC-07:00", "UTC-08:00"],
        "flag": "🇺🇸",
        "source": "Fallback Database",
    },
    "United Kingdom": {
        "name": "United Kingdom",
        "capital": "London",
        "currency_code": "GBP",
        "currency_name": "Pound sterling",
        "languages": ["English"],
        "region": "Europe",
        "subregion": "Northern Europe",
        "population": 67220000,
        "timezones": ["UTC+00:00"],
        "flag": "🇬🇧",
        "source": "Fallback Database",
    },
}


@lru_cache(maxsize=1)
def _load_index() -> dict:
    countries = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    index: dict = {}
    for item in countries:
        keys = [item.get("name"), item.get("official_name"), item.get("cca2"), item.get("cca3")]
        keys += item.get("alt_names") or []
        for key in keys:
            if key:
                index.setdefault(key.strip().lower(), item)
    return index


def find_country(query: str) -> dict | None:
    """Find a country by common/official name, alternate spelling or ISO code."""
    if not query:
        return None
    return _load_index().get(query.strip().lower())


def _to_response(item: dict) -> dict:
    currencies = item.get("currencies") or []
    currency = currencies[0] if currencies else {"code": "USD", "name": "US Dollar"}
    curated = FALLBACK_COUNTRIES.get(item["name"], {})

    return {
        "name": item["name"],
        "capital": item.get("capital") or "Unknown",
        "currency_code": currency.get("code") or "USD",
        "currency_name": currency.get("name") or "Unknown",
        "currency_symbol": currency.get("symbol") or "",
        "languages": item.get("languages") or ["Unknown"],
        "region": item.get("region") or "Unknown",
        "subregion": item.get("subregion") or "Unknown",
        "population": curated.get("population"),
        "timezones": curated.get("timezones", []),
        "flag": item.get("flag") or "",
        "country_code": item.get("cca2"),
        "official_name": item.get("official_name"),
        "source": "GlobeWise country dataset",
    }


def fallback_country(country: str) -> dict:
    return FALLBACK_COUNTRIES.get(
        country,
        {
            "name": country or "Unknown",
            "capital": "Unknown",
            "currency_code": "USD",
            "currency_name": "US Dollar",
            "languages": ["Unknown"],
            "region": "Unknown",
            "subregion": "Unknown",
            "population": None,
            "timezones": [],
            "flag": "",
            "source": "Fallback Database",
        },
    )


async def get_country_info(country: str) -> dict:
    item = find_country(country)
    if item is None:
        return fallback_country(country)
    return _to_response(item)
