from fastapi import APIRouter
from pydantic import BaseModel
from app.services.canprice_service import canprice
from app.services.aivalue_service import aivalue
from app.services.paidvalue_service import paidvalue

router = APIRouter(prefix="/internal")

class InternalValueRequest(BaseModel):
    make: str
    model: str
    year: int

@router.post("/canprice")
async def canprice_endpoint(request: InternalValueRequest):
    return await canprice(request.make, request.model, request.year)

@router.post("/aivalue")
async def aivalue_endpoint(request: InternalValueRequest):
    return await aivalue(request.make, request.model, request.year)

@router.post("/paidvalue")
async def paidvalue_endpoint(request: InternalValueRequest):
    return await paidvalue(request.make, request.model, request.year)