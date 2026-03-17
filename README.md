# Qoder: Agentic AI Coding Assistant

Qoder is a powerful, locally-hosted agentic AI coding assistant that plans, executes, and self-corrects code autonomously. It uses a sophisticated **ReAct (Reasoning and Acting)** loop to transform natural language instructions into functional, verified codebases.

## 🏗️ Architecture Overview

Qoder is built on a modular, multi-agent architecture where specialized agents collaborate to ensure high success rates:

1.  **Ambiguity Analyzer**: It scans your prompt for vagueness and asks clarifying questions *before* any code is written, preventing the agent from guessing your requirements.
2.  **Planner Agent**: It breaks down complex tasks into a structured, tool-based execution plan saved as a `project_todo.md` file. It focuses on logic flow without writing implementation code.
3.  **ReAct Agent**: This is the primary engine that executes the plan. It follows a Thinking → Action → Observation cycle, using tools to write code, run it, and read the results.
4.  **Reflection Agent**: After execution, it analyzes the output to summarize the changes and verify if the user's intent was met.
5.  **Supervisor Agent**: It tracks progression, detects infinite loops, and triggers an escalation panel if the agent hits a dead-end after multiple retries.

## 🛠️ Tool Definitions

The agents interact with the system through a suite of secure, sandboxed tools:

- `run_code(file_path)`: Executes Python, JavaScript, C++, or Java code in a sandbox. Captures `stdout`, `stderr`, and exit codes for the feedback loop.
- `write_file(path, content)`: Creates or overwrites files within the protected `/workspace` directory.
- `read_file(path)`: Retrieves the content of any file in the workspace to give the agent context.
- `list_files()`: Scans the workspace directory so the agent knows exactly which files are available.
- `install_package(package)`: Uses pip or npm to install dependencies required for the generated code.
- `todo_management`: Allows the agent to read and update the `project_todo.md` checklist to track its own progress.

## 🚦 How to Run

### 1. Prerequisites
- **Ollama**: Install [Ollama](https://ollama.com/) and download the model:
  ```bash
  ollama pull qwen2.5-coder:7b
  ```
- **Node.js**: Version 18 or higher.
- **Python**: Version 3.10 or higher.

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` to start using Qoder.

## 🧠 Memory & Context Handling

Qoder manages information across multiple layers:
- **Short-Term Memory**: A rolling history of "Thought → Action → Observation" steps maintained within the current session.
- **Working Memory**: The `project_todo.md` acts as a physical source of truth that survives session interruptions.
- **Context Pruning**: The system automatically summarizes long error logs and trims conversation history to stay within LLM token limits while keeping core instructions.

## 🔄 Switching to Gemini

If you wish to switch from local Ollama to Google Gemini:
1.  **API Key**: Add your `GEMINI_API_KEY` to `backend/app/config.py`.
2.  **Config**: Update the LLM client imports in `backend/app/agents/` from `ollama_client` to `gemini_client`.
3.  **Adapt**: Gemini is more native with JSON, so you can bypass the `repair_json` utility logic in the agent loops.
