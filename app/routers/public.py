from fastapi import APIRouter, HTTPException
from app.models import ValueRequest
from app.config import MY_API_KEY
from app.services.vrm_service import lookup_vrm
from app.services.canprice_service import canprice
from app.services.aivalue_service import aivalue
from app.services.paidvalue_service import paidvalue

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/value")
async def value_endpoint(request: ValueRequest):
    if request.apikey != MY_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    vrm = await lookup_vrm(request.numberplate)
    if vrm["result"] != "true":
        return {
            "result": "false",
            "value": 0,
            "source": "vrm_failed"
        }

    make = vrm["make"]
    model = vrm["model"]
    year = vrm["year"]

    result = await canprice(make, model, year)
    if result["result"] == "true":
        return {
            "result": "true",
            "value": result["value"],
            "source": result["source"],
            "vehicle": vrm
        }

    result = await aivalue(make, model, year)
    if result["result"] == "true":
        return {
            "result": "true",
            "value": result["value"],
            "source": result["source"],
            "vehicle": vrm
        }

    result = await paidvalue(make, model, year)
    if result["result"] == "true":
        return {
            "result": "true",
            "value": result["value"],
            "source": result["source"],
            "vehicle": vrm
        }

    return {
        "result": "false",
        "value": 0,
        "source": "all_failed",
        "vehicle": vrm
    }