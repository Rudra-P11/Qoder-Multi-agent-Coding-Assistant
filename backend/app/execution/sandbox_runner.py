from app.tools.tool_registry import TOOL_REGISTRY
from app.sandbox.command_guard import command_guard
from app.execution.runtime_detector import runtime_detector


class SandboxRunner:

    def run_tool(self, tool_name, input_data):

        if tool_name not in TOOL_REGISTRY:
            raise Exception("Invalid tool")

        # Normalize the input_data dict (make a copy to avoid mutation)
        input_data = dict(input_data)

        if tool_name == "run_code":
            # The LLM sends either "file" or "file_path" - normalize to "file_path"
            if "file" in input_data and "file_path" not in input_data:
                input_data["file_path"] = input_data.pop("file")

            file_path = input_data.get("file_path")
            runtime = runtime_detector.detect_runtime(file_path)

            if not runtime:
                return {"error": f"Unsupported runtime for file: {file_path}"}

        tool = TOOL_REGISTRY[tool_name]

        result = tool(**input_data)

        # Ensure result is always a dict (some tools may return a list or other type)
        if not isinstance(result, dict):
            result = {"status": "success", "result": result}

        return result


sandbox_runner = SandboxRunner()