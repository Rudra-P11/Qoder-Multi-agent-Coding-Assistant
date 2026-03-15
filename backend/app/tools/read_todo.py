import os
from app.sandbox.workspace_manager import workspace_manager


def read_todo():

    path = os.path.join(workspace_manager.ROOT, "project_todo.md")
    if not os.path.exists(path):
        return ""

    with open(path) as f:
        return f.read()