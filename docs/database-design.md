# Database design

GlobeWise does not use a database yet. Every request fetches live data from the public APIs, and country facts come from the bundled JSON file `backend/app/data/countries.json`.

The empty modules in `backend/app/models/` and `backend/app/db/` mark planned tables for a future version:

| Planned table | Purpose |
| --- | --- |
| `locations` | Cities a user has searched |
| `saved_places` | Cities a user has bookmarked |
| `weather_snapshots` | Cached weather results |
| `currency_rates` | Cached exchange rates |
| `safety_alerts` | Stored risk alerts |
| `travel_plans` | User trip plans |
| `ai_insights` | Generated travel tips |
| `api_logs` | Outgoing API call log |
