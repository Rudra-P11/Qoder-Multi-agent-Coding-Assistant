import subprocess


def install_package(package: str):

    process = subprocess.run(
        ["pip", "install", package],
        capture_output=True,
        text=True
    )

    return {
        "stdout": process.stdout,
        "stderr": process.stderr,
        "exit_code": process.returncode
    }