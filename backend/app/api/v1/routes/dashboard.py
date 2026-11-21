from fastapi import APIRouter, HTTPException, Query

from app.services.dashboard.dashboard_service import build_dashboard

router = APIRouter()


@router.get("/")
async def get_dashboard(city: str = Query(default="Hosur", min_length=2)):
    try:
        return await build_dashboard(city)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
