from app.llm.prompts import REFLECTION_AGENT_PROMPT
from app.llm.gemini_client import gemini_client
from app.core.workflow_logger import WorkflowLogger


class ReflectionAgent:

    def __init__(self):
        self.logger = WorkflowLogger()

    def reflect(self, code: str, output: str):
        self.logger.log("ReflectionAgent", "Reflecting on result")

        # Trim context to avoid overloading 7B models and causing timeouts
        context_summary = str(output)[-2000:]

        prompt = REFLECTION_AGENT_PROMPT.format(context_summary=context_summary)

        try:
            reflection = gemini_client.generate(prompt)

            return reflection if reflection and not reflection.startswith("ERROR") else "Execution complete. Check output above."
        except Exception:
            return "Execution complete. Check terminal output for results."


reflection_agent = ReflectionAgent()