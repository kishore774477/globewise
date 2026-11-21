from fastapi import APIRouter, HTTPException, Query

from app.providers.usgs_earthquake import get_nearby_earthquakes

router = APIRouter()


@router.get("/earthquakes")
async def earthquakes(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: int = Query(default=800),
):
    try:
        return {
            "earthquakes": await get_nearby_earthquakes(
                latitude=latitude,
                longitude=longitude,
                radius_km=radius_km,
            )
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
