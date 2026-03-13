import os


def append_file(path: str, content: str):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "a") as f:
        f.write(content)

    return {"status": "appended", "path": path}