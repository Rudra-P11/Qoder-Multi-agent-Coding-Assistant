import os

from app.memory.memory_manager import memory_manager
from app.project.project_indexer import project_indexer


class ContextBuilder:

    def build_context(self, session_id):

        conversation = memory_manager.get_conversation(session_id)

        workspace = project_indexer.index_workspace()

        todo = ""

        if os.path.exists("project_todo.md"):

            with open("project_todo.md") as f:
                todo = f.read()

        return {
            "conversation": conversation,
            "workspace": workspace,
            "todo": todo
        }


context_builder = ContextBuilder()