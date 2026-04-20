from fastapi import FastAPI
from app.config import ENABLE_INTERNAL_ROUTES
from app.routers.public import router as public_router

app = FastAPI(title="Value API")

app.include_router(public_router)

if ENABLE_INTERNAL_ROUTES:
    from app.routers.internal import router as internal_router
    app.include_router(internal_router)