import os


def read_todo():

    if not os.path.exists("project_todo.md"):
        return ""

    with open("project_todo.md") as f:
        return f.read()