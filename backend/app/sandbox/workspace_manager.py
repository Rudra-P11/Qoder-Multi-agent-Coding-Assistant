import os


class WorkspaceManager:

    ROOT = "workspace"

    def ensure_workspace(self):

        if not os.path.exists(self.ROOT):
            os.makedirs(self.ROOT)

    def resolve_path(self, path):

        full_path = os.path.join(self.ROOT, path)

        if not full_path.startswith(self.ROOT):
            raise Exception("Invalid path outside workspace")

        return full_path


workspace_manager = WorkspaceManager()