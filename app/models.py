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
    result: str
    value: int = 0
    source: str = ""