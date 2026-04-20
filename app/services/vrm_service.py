import httpx
from app.config import VRM_API_URL, VRM_API_KEY

async def lookup_vrm(numberplate: str) -> dict:
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            VRM_API_URL,
            json={
                "vrm": numberplate,
                "apikey": VRM_API_KEY
            }
        )
        response.raise_for_status()
        data = response.json()

    # Adjust field names to match your supplier response
    if data.get("result") == "true" or data.get("success") is True:
        return {
            "result": "true",
            "make": data.get("make", ""),
            "model": data.get("model", ""),
            "year": int(data.get("year", 0) or 0)
        }

    return {
        "result": "false",
        "make": "",
        "model": "",
        "year": 0
    }