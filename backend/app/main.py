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

from fastapi.responses import JSONResponse
from fastapi import Request
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = str(exc)
    trace = traceback.format_exc()
    # Log the trace locally if desired, but return a clean error to the UI
    print(f"Global Error: {error_msg}\n{trace}")
    return JSONResponse(
        status_code=500,
        content={"error": f"Internal Server Error: {error_msg}"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*"
        }
    )

@app.get("/")
def root():
    return {"status": "Qoder backend running"}