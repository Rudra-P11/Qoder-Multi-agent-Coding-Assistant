import json

from app.llm.gemini_client import gemini_client
from app.llm.prompts import REACT_AGENT_PROMPT

from app.memory.context_builder import context_builder


TOOLS_DESCRIPTION = """
Available tools:

write_file(path, content)
read_file(path)
append_file(path, content)
delete_file(path)
list_files()
search_code(query)
run_command(command)
run_code(file)
install_package(package)
read_todo()
update_todo(content)

When creating code files, always choose the correct file extension based on the language.

Examples:
Python → .py
JavaScript → .js
TypeScript → .ts
C++ → .cpp
Java → .java
Go → .go
Rust → .rs

The language should be determined from the task requirements.
"""


class ReactAgent:

    def think(self, task, session_id, context):

        project_context = context_builder.build_context(session_id)

        prompt = f"""
{REACT_AGENT_PROMPT}

Task:
{task}

Previous Context:
{context}

Project State:
{project_context}

{TOOLS_DESCRIPTION}

Respond ONLY in JSON format:

{{
  "thought": "...",
  "action": "...",
  "input": {{ }}
}}
"""

        response = gemini_client.generate(prompt)

        try:
            # Strip markdown json blocks if present
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            cleaned_response = cleaned_response.strip()

            action = json.loads(cleaned_response)

        except Exception as e:

            action = {
                "thought": f"LLM returned invalid JSON. Raw output: {response}\nError: {e}",
                "action": "none",
                "input": {}
            }

        return action