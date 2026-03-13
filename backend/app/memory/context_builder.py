import os

from app.memory.memory_manager import memory_manager
from app.project.project_indexer import project_indexer


class ContextBuilder:

    def build_context(self, session_id):

        conversation = memory_manager.get_conversation(session_id)

        workspace_tree = project_indexer.index_workspace()

        files = []

        workspace_path = "workspace"

        if os.path.exists(workspace_path):

            for root, dirs, filenames in os.walk(workspace_path):

                for file in filenames:

                    path = os.path.join(root, file)

                    files.append(path)

        # TODO file
        todo = ""

        if os.path.exists("project_todo.md"):

            with open("project_todo.md", "r") as f:
                todo = f.read()

        return {
            "conversation": conversation,
            "workspace_tree": workspace_tree,
            "files": files,
            "todo": todo
        }


context_builder = ContextBuilder()