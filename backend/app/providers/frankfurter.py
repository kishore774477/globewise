import httpx


FRANKFURTER_URL = "https://api.frankfurter.dev/v1/latest"


async def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency == to_currency:
        return {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "rate": 1,
            "converted_amount": amount,
            "source": "Frankfurter",
        }

    params = {
        "base": from_currency,
        "symbols": to_currency,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(FRANKFURTER_URL, params=params)
        response.raise_for_status()
        data = response.json()

    rate = data.get("rates", {}).get(to_currency)

    if rate is None:
        raise ValueError(f"Currency conversion not available for {from_currency} to {to_currency}")

    return {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "rate": rate,
        "converted_amount": round(amount * rate, 4),
        "source": "Frankfurter",
    }
