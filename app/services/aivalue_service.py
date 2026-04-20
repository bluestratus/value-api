async def aivalue(make: str, model: str, year: int) -> dict:
    # Replace with your real AI valuation call or local model code
    estimated_value = 14500

    if estimated_value > 0:
        return {
            "result": "true",
            "value": estimated_value,
            "source": "aivalue"
        }

    return {
        "result": "false",
        "value": 0,
        "source": "aivalue"
    }