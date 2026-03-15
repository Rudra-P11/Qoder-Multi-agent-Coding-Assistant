from app.sandbox.workspace_manager import workspace_manager

def list_files():
    files = workspace_manager.list_files()
    return {
        "status": "success",
        "files": files,
        "count": len(files)
    }