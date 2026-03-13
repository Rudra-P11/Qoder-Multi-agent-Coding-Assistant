from app.tools.tool_registry import TOOL_REGISTRY
from app.sandbox.command_guard import command_guard
from app.sandbox.tool_result_store import tool_result_store


class SandboxRunner:

    def run_tool(self, tool_name, input_data):

        if tool_name not in TOOL_REGISTRY:
            raise Exception("Invalid tool")

        if tool_name == "run_command":

            command = input_data.get("command")

            if not command_guard.validate(command):
                raise Exception("Unsafe command blocked")

        tool = TOOL_REGISTRY[tool_name]

        result = tool(**input_data)

        tool_result_store.store(tool_name, result)

        return result


sandbox_runner = SandboxRunner()