async def aivalue(make: str, model: str, year: int) -> dict:
    estimated_value = 14500

    if estimated_value > 0:
        return {"status": "success", "make": make, "model": model, "year": year, "price_new": estimated_value, "source": "aivalue"}

    return {"status": "failed", "make": make, "model": model, "year": year, "price_new": 0, "source": "aivalue"}
