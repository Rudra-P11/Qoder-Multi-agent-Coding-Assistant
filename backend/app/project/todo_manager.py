import os
from app.sandbox.workspace_manager import workspace_manager

TODO_FILE = os.path.join(workspace_manager.ROOT, "project_todo.md")

class TodoManager:

    def create_todo(self, steps):

        lines = []

        for step in steps:
            lines.append(f"[ ] {step}")

        with open(TODO_FILE, "w") as f:
            f.write("\n".join(lines))

    def mark_completed(self, step):

        if not os.path.exists(TODO_FILE):
            return

        with open(TODO_FILE, "r") as f:
            lines = f.readlines()

        updated = []

        for line in lines:

            if step in line:
                updated.append(line.replace("[ ]", "[x]"))
            else:
                updated.append(line)

        with open(TODO_FILE, "w") as f:
            f.writelines(updated)

todo_manager = TodoManager()