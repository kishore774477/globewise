# Deployment notes

## Docker Compose

From the repository root:

```bash
docker compose -f docker/docker-compose.yml up --build
```

- Dashboard: http://localhost:8080
- API: http://localhost:8000 (docs at http://localhost:8000/docs)

The frontend image builds the Vite app and serves it with nginx, which forwards `/api` requests to the backend container (`docker/nginx.conf`).

## Separate hosting

- **Backend**: any host that runs Python 3.11+. Start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`, run from the `backend/` folder.
- **Frontend**: run `npm run build` in `frontend/` and serve the `dist/` folder as a static site. Set `VITE_API_BASE_URL` to the backend URL (for example `https://api.example.com/api/v1`) before building.
- **CORS**: the backend only allows `localhost:5173`/`5174` by default. Add the frontend's domain to `allow_origins` in `backend/app/main.py` when hosting them on different domains.

No API keys or secrets are needed.
