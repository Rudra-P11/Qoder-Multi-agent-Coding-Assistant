from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.api.workspace_routes import router as workspace_router
from app.api.websocket import router as websocket_router

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(api_router, prefix="/api")

# Workspace routes
app.include_router(workspace_router, prefix="/api/workspace")

# WebSocket
app.include_router(websocket_router)

@app.get("/")
def root():
    return {"status": "Qoder backend running"}