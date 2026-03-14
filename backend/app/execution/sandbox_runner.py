from app.tools.tool_registry import TOOL_REGISTRY
from app.safety.command_guard import command_guard
from app.execution.runtime_detector import runtime_detector


class SandboxRunner:

    def run_tool(self, tool_name, input_data):

        if tool_name not in TOOL_REGISTRY:
            raise Exception("Invalid tool")

        if tool_name == "run_code":

            file_path = input_data.get("file")

            runtime = runtime_detector.detect_runtime(file_path)

            if not runtime:
                raise Exception("Unsupported runtime")

        tool = TOOL_REGISTRY[tool_name]

        result = tool(**input_data)

        return result


sandbox_runner = SandboxRunner()