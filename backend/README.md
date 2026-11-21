# GlobeWise backend

FastAPI service behind the GlobeWise dashboard.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

See [`../docs/backend-flow.md`](../docs/backend-flow.md) for how a dashboard request is built and [`../docs/api-list.md`](../docs/api-list.md) for all endpoints.
