from fastapi import FastAPI

from app.api.routes import router as api_router
from app.api.websocket import router as ws_router

from app.database.database import engine
from app.database.models import Base

app = FastAPI(title="Qoder Agent System")

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api")

app.include_router(ws_router)