from fastapi import FastAPI

from app.api.routes import router as api_router
from app.api.websocket import router as ws_router

app = FastAPI(title="Qoder Agent System")

app.include_router(api_router, prefix="/api")

app.include_router(ws_router)