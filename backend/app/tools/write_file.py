import os

def write_file(path: str, content: str):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        f.write(content)

    return {"status": "file_written", "path": path}