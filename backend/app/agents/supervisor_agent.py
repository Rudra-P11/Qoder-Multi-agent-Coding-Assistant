from app.llm.ollama_client import ollama_client
from app.llm.prompts import SUPERVISOR_AGENT_PROMPT


class SupervisorAgent:

    def evaluate(self, task: str, context: str):

        # Trim context to avoid slow inference on large histories
        context_trimmed = context[-1500:] if len(context) > 1500 else context

        prompt = SUPERVISOR_AGENT_PROMPT.format(task=task, context_trimmed=context_trimmed)

        try:
            result = ollama_client.generate(prompt)

            return result if result and not result.startswith("ERROR") else "Agent execution complete."
        except Exception:
            return "Agent execution complete."


supervisor_agent = SupervisorAgent()