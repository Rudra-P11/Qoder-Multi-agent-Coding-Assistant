import subprocess
import os

from app.execution.runtime_detector import runtime_detector


def run_code(file_path: str):

    runtime = runtime_detector.detect_runtime(file_path)

    if not runtime:

        return {
            "error": f"No runtime found for {file_path}"
        }

    try:

        if runtime[0] in ["g++", "gcc"]:

            exe = file_path.replace(".cpp", "").replace(".c", "")

            subprocess.run(
                [runtime[0], file_path, "-o", exe],
                capture_output=True,
                text=True
            )

            result = subprocess.run(
                [exe],
                capture_output=True,
                text=True
            )

        elif runtime[0] == "javac":

            subprocess.run(
                ["javac", file_path],
                capture_output=True,
                text=True
            )

            class_name = os.path.basename(file_path).replace(".java", "")

            result = subprocess.run(
                ["java", class_name],
                capture_output=True,
                text=True
            )

        else:

            result = subprocess.run(
                runtime + [file_path],
                capture_output=True,
                text=True
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