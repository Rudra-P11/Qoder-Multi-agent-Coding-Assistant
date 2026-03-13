from app.llm.gemini_client import gemini_client


class TaskInterpreterAgent:

    def interpret(self, task):

        prompt = f"""
Analyze the following coding request.

Task:
{task}

Return JSON with:
language
framework
dependencies

Example output:

{{
 "language": "python",
 "framework": "none",
 "dependencies": ["requests"]
}}
"""

        response = gemini_client.generate(prompt)

        return response