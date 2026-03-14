import subprocess
import tempfile


def run_code(code: str):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:

        f.write(code.encode())

        path = f.name

    try:

        result = subprocess.run(
            ["python", path],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }

    except Exception as e:

        return {
            "error": str(e)
        }