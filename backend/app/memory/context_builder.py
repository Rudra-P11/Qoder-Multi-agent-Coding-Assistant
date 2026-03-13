import os

from app.memory.memory_manager import memory_manager

class ContextBuilder:

    def build_context(self, session_id):

        conversation = memory_manager.get_conversation(session_id)

        files = []

        if os.path.exists("workspace"):

            for file in os.listdir("workspace"):
                files.append(file)

        todo = ""

        if os.path.exists("project_todo.md"):

            with open("project_todo.md") as f:
                todo = f.read()

        return {
            "conversation": conversation,
            "files": files,
            "todo": todo
        }


context_builder = ContextBuilder()