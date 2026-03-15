import os

from app.core.event_bus import event_bus
from app.sandbox.workspace_manager import workspace_manager

def create_file(path: str):

    workspace_manager.write_file(path, "")

    import asyncio

    asyncio.create_task(
        event_bus.broadcast({
            "agent": "workspace",
            "message": "file_created",
            "data": {
                "path": path
            }
        })
    )

    return {"status": "created"}