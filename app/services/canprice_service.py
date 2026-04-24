import os
import httpx
from typing import Optional, Dict, Any


async def canprice(make: str, model: str, year: int, debug: bool = False) -> dict:
    """
    Call PHP canprice service instead of direct database access
    """
    php_url = os.getenv("PHP_SERVICE_URL", "http://php:80")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{php_url}/pricenew.php",
                json={
                    "make": make,
                    "model": model,
                    "year": year,
                    "debug": debug
                },
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("result") == "true" and "price_new" in result:
                    return {"status": "success", "make": make, "model": model, "year": year, "price_new": int(result["price_new"]), "source": "canprice"}
                else:
                    return {"status": "failed", "make": make, "model": model, "year": year, "price_new": 0, "source": "canprice"}
            else:
                return {"status": "error", "make": make, "model": model, "year": year, "price_new": 0, "source": "canprice"}

    except httpx.TimeoutException:
        return {"status": "error", "make": make, "model": model, "year": year, "price_new": 0, "source": "canprice"}
    except httpx.RequestError:
        return {"status": "error", "make": make, "model": model, "year": year, "price_new": 0, "source": "canprice"}
    except Exception:
        return {"status": "error", "make": make, "model": model, "year": year, "price_new": 0, "source": "canprice"}