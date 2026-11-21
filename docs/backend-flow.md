# Backend flow

The backend is a FastAPI app (`backend/app/main.py`). Routes live in `app/api/v1/routes/`, external API clients in `app/providers/`, and the dashboard logic in `app/services/dashboard/dashboard_service.py`.

## Dashboard request (`GET /api/v1/dashboard/?city=Tokyo`)

1. **Geocode** the city name with the Open-Meteo geocoding API (`providers/open_meteo.py`). If nothing matches, return an empty dashboard with a "location not found" message.
2. **Weather**: fetch current conditions and a 7-day forecast from Open-Meteo for the city's coordinates.
3. **Country info**: look the country up in the bundled dataset `app/data/countries.json` (`providers/rest_countries.py`). The public REST Countries API is no longer free, so the data ships with the project.
4. **Currency**: convert 1 unit of the local currency to USD (or INR, if the local currency is USD) with Frankfurter (`providers/frankfurter.py`).
5. **Earthquakes**: download the USGS feed of M4.5+ earthquakes from the past week and keep the 5 closest within 800 km (`providers/usgs_earthquake.py`).
6. **Safety score**: start at 10 and add points for heavy rain, strong wind, thunderstorms and nearby strong earthquakes, capped at 100. The score maps to a level: Low (< 25), Medium (25–49), High (50–74), Critical (75+).
7. **Travel tip**: build a one-paragraph summary from the level, weather and main risk reason.

Each step after geocoding is wrapped in its own `try`/`except`, so one failing data source shows as "unavailable" instead of breaking the whole dashboard.
