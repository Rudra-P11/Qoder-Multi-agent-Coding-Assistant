import os
from app.sandbox.workspace_manager import workspace_manager

def delete_file(path: str):
    try:
        full_path = workspace_manager.resolve_path(path)

        if os.path.exists(full_path):

            os.remove(full_path)

            return {"status": "deleted"}

        return {"status": "not_found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}