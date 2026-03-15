import subprocess
import os

from app.execution.runtime_detector import runtime_detector
from app.sandbox.workspace_manager import workspace_manager


def run_code(file_path: str):
    # Always resolve to the full absolute workspace path
    try:
        abs_path = workspace_manager.resolve_path(file_path)
    except Exception:
        # If resolve fails (e.g. already absolute), use the path as-is
        abs_path = file_path

    if not os.path.exists(abs_path):
        return {
            "error": f"File not found in workspace: {file_path} (resolved: {abs_path})",
            "exit_code": 2
        }

    runtime = runtime_detector.detect_runtime(abs_path)

    if not runtime:
        return {
            "error": f"No runtime found for {file_path}. Supported: .py, .js, .cpp, .java, .go, .rs"
        }

    cwd = workspace_manager.ROOT  # run scripts from workspace dir so relative imports work

    try:

        if runtime[0] in ["g++", "gcc"]:
            exe = abs_path.replace(".cpp", "").replace(".c", "")
            exe_target = exe + ".exe" if os.name == 'nt' else exe

            subprocess.run(
                [runtime[0], abs_path, "-o", exe_target],
                capture_output=True, text=True, timeout=30, cwd=cwd
            )

            result = subprocess.run(
                [exe_target],
                capture_output=True, text=True, timeout=30, cwd=cwd
            )

        elif runtime[0] == "javac":
            subprocess.run(
                ["javac", abs_path],
                capture_output=True, text=True, timeout=30, cwd=cwd
            )

            class_name = os.path.basename(abs_path).replace(".java", "")
            result = subprocess.run(
                ["java", class_name],
                capture_output=True, text=True, timeout=30, cwd=cwd
            )

        else:
            result = subprocess.run(
                runtime + [abs_path],
                capture_output=True, text=True, timeout=30, cwd=cwd
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