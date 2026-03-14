import os
import asyncio

from app.core.event_bus import event_bus

WORKSPACE_ROOT = "workspace"


def write_file(path: str, content: str):

    full_path = os.path.join(WORKSPACE_ROOT, path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

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