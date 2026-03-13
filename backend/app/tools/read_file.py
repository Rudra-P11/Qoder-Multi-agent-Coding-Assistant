def read_file(path: str):

    try:

        with open(path, "r") as f:
            content = f.read()

        return {
            "status": "success",
            "content": content
        }

    except Exception as e:

        return {
            "status": "error",
            "error": str(e)
        }