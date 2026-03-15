from app.llm.ollama_client import ollama_client
from app.core.workflow_logger import WorkflowLogger


class ReflectionAgent:

    def __init__(self):
        self.logger = WorkflowLogger()

    def reflect(self, code: str, output: str):
        self.logger.log("ReflectionAgent", "Reflecting on result")

        # Trim context to avoid overloading 7B models and causing timeouts
        context_summary = str(output)[-2000:]

        prompt = f"""You are a code reviewer. In 2-3 sentences, summarize what the agent did and whether it succeeded.

Execution context (last 2000 chars):
{context_summary}

Summary:"""

        try:
            result = ollama_client.generate(prompt)
            return result if result and not result.startswith("ERROR") else "Execution complete. Check output above."
        except Exception:
            return "Execution complete. Check terminal output for results."


reflection_agent = ReflectionAgent()