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
            exe_target = exe + ".exe" if os.name == 'nt' else exe

            subprocess.run(
                [runtime[0], file_path, "-o", exe_target],
                capture_output=True,
                text=True,
                timeout=30
            )

            result = subprocess.run(
                [exe_target],
                capture_output=True,
                text=True,
                timeout=30
            )

        elif runtime[0] == "javac":

            subprocess.run(
                ["javac", file_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            class_name = os.path.basename(file_path).replace(".java", "")

            result = subprocess.run(
                ["java", class_name],
                capture_output=True,
                text=True,
                timeout=30
            )

        else:

            result = subprocess.run(
                runtime + [file_path],
                capture_output=True,
                text=True,
                timeout=30
            )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }

    except subprocess.TimeoutExpired as e:

        return {
            "error": f"Execution timed out after {e.timeout} seconds",
            "exit_code": 124
        }
        
    except Exception as e:

        return {
            "error": str(e)
        }