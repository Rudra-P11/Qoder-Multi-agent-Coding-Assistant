import os
import asyncio

from app.core.event_bus import event_bus
from app.sandbox.workspace_manager import workspace_manager

def write_file(path: str, content: str):

    workspace_manager.write_file(path, content)

    asyncio.create_task(
        event_bus.broadcast({
            "agent": "workspace",
            "message": "file_updated",
            "data": {
                "path": path
            }
        })
    )

    return {
        "status": "written",
        "path": path
    }