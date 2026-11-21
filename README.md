# GlobeWise

GlobeWise is a personal global life assistant. Search any city to see live weather, a 7-day forecast, a safety risk score, nearby earthquake activity, country facts and currency conversion on one dashboard.

## Tech stack

- **Backend:** Python, FastAPI, httpx, Uvicorn
- **Frontend:** React 19, TypeScript, Vite, Axios, lucide-react
- **Data sources (no API keys needed):**
  - [Open-Meteo](https://open-meteo.com/) for geocoding and weather
  - [Frankfurter](https://frankfurter.dev/) for exchange rates
  - [USGS Earthquake feed](https://earthquake.usgs.gov/earthquakes/feed/) for earthquake activity
  - A bundled country dataset (`backend/app/data/countries.json`, derived from [mledoze/countries](https://github.com/mledoze/countries), ODbL)

## Project structure

```
globewise/
├── backend/            FastAPI app
│   ├── app/
│   │   ├── api/v1/     API routes
│   │   ├── providers/  Clients for external data sources
│   │   ├── services/   Dashboard logic and safety scoring
│   │   └── data/       Bundled country dataset
│   ├── globewise_live.py  Extra /api/* endpoints
│   └── requirements.txt
├── frontend/           React + Vite dashboard
├── docs/               Project notes
└── start-dev.ps1       Starts backend and frontend together (Windows)
```

## Getting started

Requirements: Python 3.11+ and Node.js 20+.

### 1. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

On macOS or Linux, use `.venv/bin/python` instead of `.\.venv\Scripts\python.exe`.

The API runs at http://127.0.0.1:8000, with interactive docs at http://127.0.0.1:8000/docs.

### 2. Frontend

```powershell
cd frontend
copy .env.example .env
npm install
npm run dev
```

Open http://localhost:5173. The Vite dev server forwards `/api` requests to the backend on port 8000.

### Run both at once (Windows)

After the one-time setup above:

```powershell
.\start-dev.ps1
```

## API endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Health check |
| GET | `/api/v1/dashboard/?city=Tokyo` | Full dashboard for a city |
| GET | `/api/v1/locations/search?query=Paris` | City search |
| GET | `/api/v1/weather/?latitude=..&longitude=..` | Current weather and forecast |
| GET | `/api/v1/safety/earthquakes?latitude=..&longitude=..` | Nearby earthquakes |
| GET | `/api/v1/currency/convert?amount=10&from_currency=INR&to_currency=USD` | Currency conversion |
| GET | `/api/v1/country-info/?country=Japan` | Country facts |
| GET | `/api/analyze?city=Tokyo` | Combined city analysis |

## Configuration

`frontend/.env`:

| Variable | Default | Purpose |
| --- | --- | --- |
| `VITE_API_BASE_URL` | `/api/v1` | Backend base URL. Set a full URL when the backend is hosted separately. |
| `VITE_APP_NAME` | `GlobeWise` | App name |
