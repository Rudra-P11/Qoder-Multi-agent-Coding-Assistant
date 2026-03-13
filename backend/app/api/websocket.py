from fastapi import WebSocket, APIRouter
from app.core.event_bus import event_bus

router = APIRouter()

@router.websocket("/ws")

async def websocket_endpoint(websocket: WebSocket):

    await event_bus.connect(websocket)

    try:

        while True:
            await websocket.receive_text()

    except:

        event_bus.disconnect(websocket)