from app.sandbox.workspace_manager import workspace_manager

def read_file(path: str):

    try:
        content = workspace_manager.read_file(path)

        return {
            "status": "success",
            "content": content
        }

    except Exception as e:

        return {
            "status": "error",
            "error": str(e)
        }