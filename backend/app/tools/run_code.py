import subprocess


def run_code(file_path: str):

    process = subprocess.run(
        ["python", file_path],
        capture_output=True,
        text=True,
        timeout=20
    )

    return {
        "stdout": process.stdout,
        "stderr": process.stderr,
        "exit_code": process.returncode
    }