import os
from app.sandbox.workspace_manager import workspace_manager

def search_code(query: str):

    results = []

    for root, _, files in os.walk(workspace_manager.ROOT):

        for file in files:

            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, workspace_manager.ROOT)

            with open(path, "r", errors="ignore") as f:

                if query in f.read():

                    # Always return relative path formats
                    results.append(rel_path.replace("\\", "/"))

    return results