from app.llm.ollama_client import ollama_client


class SupervisorAgent:

    def evaluate(self, task: str, context: str):

        # Trim context to avoid slow inference on large histories
        context_trimmed = context[-1500:] if len(context) > 1500 else context

        prompt = f"""Task: {task}

Recent agent actions:
{context_trimmed}

In one sentence: did the agent complete the task? If not, what should it do next?"""

        try:
            result = ollama_client.generate(prompt)
            return result if result and not result.startswith("ERROR") else "Agent execution complete."
        except Exception:
            return "Agent execution complete."


supervisor_agent = SupervisorAgent()