from typing import List
from fastapi import WebSocket

from app.timeline.timeline_manager import timeline_manager


class EventBus:

    def __init__(self):

        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):

        await websocket.accept()

        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):

        self.connections.remove(websocket)

    async def broadcast(self, event):

        timeline_manager.add_event(
            event.get("agent"),
            event.get("message"),
            event.get("data")
        )

        for connection in self.connections:

            await connection.send_json(event)


event_bus = EventBus()