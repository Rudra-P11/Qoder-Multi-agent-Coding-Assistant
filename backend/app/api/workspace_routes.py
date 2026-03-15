from fastapi import APIRouter
from app.sandbox.workspace_manager import workspace_manager
from app.tools.run_code import run_code

router = APIRouter()


@router.get("/files")
def list_files():
    """
    Return all files in the workspace
    """
    files = workspace_manager.list_files()
    return {"files": files}


@router.get("/file")
def read_file(path: str):
    """
    Read a single file
    """
    content = workspace_manager.read_file(path)
    return {"content": content}


@router.post("/file")
def write_file(path: str, content: str):
    """
    Write/update file
    """
    workspace_manager.write_file(path, content)
    return {"status": "saved"}


@router.post("/run")
def run_script(path: str):
    """
    Execute a script directly from the frontend
    """
    full_path = workspace_manager.resolve_path(path)
    result = run_code(full_path)
    return result

@router.delete("/file")
def delete_file(path: str):
    """
    Delete a file
    """
    success = workspace_manager.delete_file(path)
    if not success:
        return {"status": "not_found"}
    return {"status": "deleted"}