import os
from app.sandbox.workspace_manager import workspace_manager

def update_todo(task):

    path = os.path.join(workspace_manager.ROOT, "project_todo.md")
    with open(path, "a") as f:
        f.write(f"\n[ ] {task}")

    return {"status": "task_added"}