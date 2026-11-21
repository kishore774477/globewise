from fastapi import APIRouter, HTTPException, Query

from app.providers.open_meteo import get_weather

router = APIRouter()


@router.get("/")
async def weather(
    latitude: float = Query(...),
    longitude: float = Query(...),
):
    try:
        return await get_weather(latitude=latitude, longitude=longitude)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
