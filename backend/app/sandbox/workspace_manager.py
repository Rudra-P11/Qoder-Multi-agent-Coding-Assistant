import os

class WorkspaceManager:

    # Locate the root workspace directory at the same level as the backend and frontend folders
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    ROOT = os.path.join(BASE_DIR, "workspace")

    def ensure_workspace(self):

        if not os.path.exists(self.ROOT):
            os.makedirs(self.ROOT)

    def resolve_path(self, path):

        full_path = os.path.join(self.ROOT, path)

        if not full_path.startswith(self.ROOT):
            raise Exception("Invalid path outside workspace")

        return full_path

    def read_file(self, path):
        full_path = self.resolve_path(path)
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, path, content):
        self.ensure_workspace()
        full_path = self.resolve_path(path)
        # Ensure parent directories exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
            
    def list_files(self):
        self.ensure_workspace()
        files = []
        for root, _, filenames in os.walk(self.ROOT):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, self.ROOT)
                # Ensure we use forward slashes for paths in UI
                files.append(rel_path.replace("\\", "/"))
        return files
    def delete_file(self, path):
        full_path = self.resolve_path(path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False


workspace_manager = WorkspaceManager()