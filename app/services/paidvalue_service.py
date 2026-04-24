import httpx
from app.config import PAIDVALUE_API_URL, PAIDVALUE_API_KEY

async def paidvalue(make: str, model: str, year: int) -> dict:
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                PAIDVALUE_API_URL,
                json={
                    "make": make,
                    "model": model,
                    "year": year,
                    "apikey": PAIDVALUE_API_KEY
                }
            )
            response.raise_for_status()
            data = response.json()
    except (httpx.HTTPStatusError, httpx.RequestError):
        return {"status": "error", "make": make, "model": model, "year": year, "price_new": 0, "source": "paidvalue"}

    if data.get("result") == "true":
        return {"status": "success", "make": make, "model": model, "year": year, "price_new": int(data.get("value", 0) or 0), "source": "paidvalue"}

    return {"status": "failed", "make": make, "model": model, "year": year, "price_new": 0, "source": "paidvalue"}