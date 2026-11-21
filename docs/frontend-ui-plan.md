# Frontend UI

The frontend is a single-page React + TypeScript app built with Vite. The entry point is `src/main.tsx`, which renders `src/app/App.tsx` and the dashboard in `src/pages/DashboardPage.tsx`.

## Layout

- **Sidebar**: app name and section shortcuts
- **Header**: title and a Refresh button that reloads the current city
- **Search**: a city search box with an Analyze button
- **Cards**: location, current weather, safety score, currency, travel insight
- **Country intelligence**: capital, region, currency, languages
- **7-day forecast**: daily max/min temperature and chance of rain
- **Safety monitoring**: nearby earthquakes with magnitude and distance

## Data

`src/services/dashboardApi.ts` calls `GET /dashboard/?city=...` through the Axios client in `src/services/apiClient.ts`. The response type is defined in `src/types/dashboard.ts`.

In development, Vite forwards `/api` to the backend on port 8000 (`vite.config.ts`). For a separately hosted backend, set `VITE_API_BASE_URL` in `frontend/.env`.

Styles are in `src/styles/globals.css`.
