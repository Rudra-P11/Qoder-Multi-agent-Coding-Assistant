from app.tools.tool_registry import TOOL_REGISTRY

class SandboxRunner:

    def run_tool(self, tool_name, input_data):

        if tool_name not in TOOL_REGISTRY:
            raise Exception("Invalid tool")

        tool = TOOL_REGISTRY[tool_name]

        result = tool(**input_data)

        return result

sandbox_runner = SandboxRunner()