from fastapi import APIRouter
from app.workspace.workspace_manager import workspace_manager

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