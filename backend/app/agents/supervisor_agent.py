from app.llm.gemini_client import gemini_client


class SupervisorAgent:

    def evaluate(self, task, context):

        prompt = f"""
Task:
{task}

Agent Execution Context:
{context}

Determine if the agent is stuck.

If stuck:
Provide a new strategy.
Return a short recommendation.
"""

        return gemini_client.generate(prompt)


supervisor_agent = SupervisorAgent()