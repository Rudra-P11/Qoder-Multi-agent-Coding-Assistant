from app.llm.gemini_client import gemini_client
from app.llm.prompts import DEBUGGER_AGENT_PROMPT
from app.core.workflow_logger import WorkflowLogger


class DebuggerAgent:

    def __init__(self):

        self.logger = WorkflowLogger()

    def fix_code(self, code: str, error: str):

        self.logger.log("DebuggerAgent", "Fixing code")

        prompt = DEBUGGER_AGENT_PROMPT.format(code=code, error=error)

        new_code = gemini_client.generate(prompt)


        return new_code


debugger_agent = DebuggerAgent()