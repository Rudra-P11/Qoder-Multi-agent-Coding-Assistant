import os
from app.sandbox.workspace_manager import workspace_manager

def append_file(path: str, content: str):

    full_path = workspace_manager.resolve_path(path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "a") as f:
        f.write(content)

    return {"status": "appended", "path": path}