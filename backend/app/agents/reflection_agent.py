from app.llm.gemini_client import gemini_client


class ReflectionAgent:

    def reflect(self, task, result):

        prompt = f"""
Task:
{task}

Result:
{result}

Analyze the execution.

What went wrong?
What could be improved?

Return a short reflection.
"""

        return gemini_client.generate(prompt)