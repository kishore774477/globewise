from fastapi import APIRouter, HTTPException, Query

from app.providers.frankfurter import convert_currency

router = APIRouter()


@router.get("/convert")
async def currency_convert(
    amount: float = Query(default=1, gt=0),
    from_currency: str = Query(default="INR", min_length=3, max_length=3),
    to_currency: str = Query(default="USD", min_length=3, max_length=3),
):
    try:
        return await convert_currency(
            amount=amount,
            from_currency=from_currency,
            to_currency=to_currency,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
