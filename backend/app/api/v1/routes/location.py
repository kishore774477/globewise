from fastapi import APIRouter, HTTPException, Query

from app.providers.open_meteo import search_locations

router = APIRouter()


@router.get("/search")
async def location_search(query: str = Query(..., min_length=2)):
    try:
        results = await search_locations(query, count=8)
        return {
            "query": query,
            "results": results,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
