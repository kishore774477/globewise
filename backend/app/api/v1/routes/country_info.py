from fastapi import APIRouter, HTTPException, Query

from app.providers.rest_countries import get_country_info

router = APIRouter()


@router.get("/")
async def country_info(country: str = Query(default="India", min_length=2)):
    try:
        return await get_country_info(country)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
