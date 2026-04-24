from pydantic import BaseModel

class ValueRequest(BaseModel):
    numberplate: str
    apikey: str

class VRMResult(BaseModel):
    result: str
    make: str = ""
    model: str = ""
    year: int = 0

class PriceResult(BaseModel):
    status: str  # "success", "failed", "error"
    make: str = ""
    model: str = ""
    year: int = 0
    price_new: int = 0
    source: str = ""