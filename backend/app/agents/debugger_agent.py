from app.llm.ollama_client import ollama_client
from app.core.workflow_logger import WorkflowLogger


class DebuggerAgent:

    def __init__(self):

        self.logger = WorkflowLogger()

    def fix_code(self, code: str, error: str):

        self.logger.log("DebuggerAgent", "Fixing code")

        prompt = f"""
The following code produced an error.

Code:
{code}

Error:
{error}

Fix the code and return the corrected version.
"""

        new_code = ollama_client.generate(prompt)

        return new_code


debugger_agent = DebuggerAgent()