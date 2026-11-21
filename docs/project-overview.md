# Project overview

GlobeWise is a personal global life assistant. A user searches for any city and gets one dashboard with:

- Current weather and a 7-day forecast
- A safety risk score (Low / Medium / High / Critical) with the reasons behind it
- Recent earthquake activity near the city
- Country facts: capital, region, languages, currency
- A live currency conversion from the local currency to USD
- A short travel tip that summarises the above

All data comes from free public sources that need no API keys (Open-Meteo, Frankfurter, USGS) plus a bundled country dataset, so the project runs without any account setup.

## Parts

| Part | Folder | Tech |
| --- | --- | --- |
| Backend API | `backend/` | Python, FastAPI, httpx |
| Web dashboard | `frontend/` | React 19, TypeScript, Vite |
| Containers | `docker/` | Dockerfiles and Docker Compose |
| API requests | `postman/` | Postman collection |

See [backend-flow.md](backend-flow.md), [frontend-ui-plan.md](frontend-ui-plan.md) and [api-list.md](api-list.md) for details.
