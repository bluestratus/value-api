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
                f"{php_url}/canprice.php",
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
                if "result" in result and "price_new" in result:
                    return {"result": result["result"], "value": int(result["price_new"]), "source": "canprice"}
                else:
                    return {"result": "false", "value": 0, "error": "invalid_response_format"}
            else:
                return {
                    "result": "false",
                    "value": 0,
                    "error": f"http_{response.status_code}",
                    "details": response.text[:200]
                }

    except httpx.TimeoutException:
        return {"result": "false", "value": 0, "error": "timeout"}
    except httpx.RequestError as e:
        return {"result": "false", "value": 0, "error": "connection_failed", "details": str(e)}
    except Exception as e:
        return {"result": "false", "value": 0, "error": "unexpected_error", "details": str(e)}