# API list

Base URL in development: `http://127.0.0.1:8000`. Interactive docs: `http://127.0.0.1:8000/docs`.
A ready-made Postman collection is in [`postman/globewise-api-collection.json`](../postman/globewise-api-collection.json).

## Core

| Method | Path | Query parameters | Returns |
| --- | --- | --- | --- |
| GET | `/` | – | Service banner |
| GET | `/health` | – | `{"status": "ok"}` |

## Version 1 (`/api/v1`)

| Method | Path | Query parameters | Returns |
| --- | --- | --- | --- |
| GET | `/dashboard/` | `city` (default `Hosur`) | Location, weather, country info, currency, safety and travel tip in one response. Used by the frontend. |
| GET | `/locations/search` | `query` | Up to 8 matching cities |
| GET | `/weather/` | `latitude`, `longitude` | Current weather and 7-day forecast |
| GET | `/safety/earthquakes` | `latitude`, `longitude`, `radius_km` (default 800) | Up to 5 nearest M4.5+ earthquakes from the past week |
| GET | `/currency/convert` | `amount`, `from_currency`, `to_currency` | Converted amount and rate |
| GET | `/country-info/` | `country` | Capital, region, languages, currency, flag |
| GET | `/saved-places/` | – | Placeholder, returns an empty list |
| POST | `/translation/` | – | Placeholder demo response |
| POST | `/travel-guide/` | – | Placeholder demo response |

## City endpoints (`/api`)

Defined in `backend/globewise_live.py`. Each takes a `city` query parameter.

| Method | Path | Returns |
| --- | --- | --- |
| GET | `/city/resolve` | Resolved city with coordinates |
| GET | `/analyze` | City, weather, country, currency and safety together |
| GET | `/weather` | Weather for the city |
| GET | `/country` | Country facts for the city |
| GET | `/currency` | Exchange rate from the city's currency to `target_currency` (default `USD`) |
| GET | `/safety` | Safety assessment for the city |
