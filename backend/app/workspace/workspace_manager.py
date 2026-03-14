import os

WORKSPACE_DIR = "workspace"


class WorkspaceManager:

    def __init__(self):
        os.makedirs(WORKSPACE_DIR, exist_ok=True)

    def list_files(self):

        files = []

        for root, _, filenames in os.walk(WORKSPACE_DIR):
            for f in filenames:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, WORKSPACE_DIR)
                files.append(rel)

        return files

    def read_file(self, path):

        full = os.path.join(WORKSPACE_DIR, path)

        if not os.path.exists(full):
            return ""

        with open(full, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, path, content):

        full = os.path.join(WORKSPACE_DIR, path)

        os.makedirs(os.path.dirname(full), exist_ok=True)

        with open(full, "w", encoding="utf-8") as f:
            f.write(content)


workspace_manager = WorkspaceManager()