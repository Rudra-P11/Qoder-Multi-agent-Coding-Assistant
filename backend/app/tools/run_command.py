import subprocess


def run_command(command: str):

    process = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "stdout": process.stdout,
        "stderr": process.stderr,
        "exit_code": process.returncode
    }