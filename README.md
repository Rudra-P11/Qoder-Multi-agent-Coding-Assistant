# Qoder: Agentic AI Coding Assistant

Qoder is a powerful, locally-hosted agentic AI coding assistant designed to bridge the gap between human instruction and automated execution. Powered by **Ollama** and a specialized **ReAct (Reasoning and Acting)** agent loop, Qoder can plan, write, execute, and self-correct code autonomously.

## 🚀 Project Overview

### 1. Multi-Agent Architecture and Planning
The core of the system is a modular backend where tasks are decomposed into structured execution plans. A **Task Interpreter** extracts technical metadata (language, libraries) to ground the assistant’s strategy. This leads into a **Planning Phase**, where a specialized agent generates a JSON array of discrete tasks.

### 2. Sandboxed Execution and User Interface
Code execution occurs in an isolated Python subprocess restricted to a dedicated workspace directory with strict path validation and timeouts. The system features a **React-based web UI** with a live terminal and the **Monaco Editor**, providing full visibility into the agent's work.

### 3. Self-Correction and Feedback Loop
A recursive agent loop handles errors by feeding `stderr` back into a **Debugger Agent**. To prevent repeating failed logic, a **Reflector Agent** analyzes why a previous attempt failed before proposing a specific technical change for the next iteration.

### 4. Memory and Context Management
The assistant manages its state through a multi-tiered memory system:
* **Short-Term Memory:** Maintains a rolling conversation history within each agent's loop.
* **Working Memory:** Uses persistent files like `project_todo.md` to store state.
* **Context Pruning:** Automatically handles LLM token limits while retaining critical instructions.

### 5. Out-of-the-Box: Ambiguity Analysis
To handle underspecified prompts, Qoder features an **Ambiguity Analyzer**. It scores requests based on clarity; if a prompt is too vague, the system interrupts the workflow to ask the user targeted, multiple-choice clarifying questions.

---

## 🚦 How to Run

### 1. Prerequisites

(If you want to use locally downloaded model)
- **Ollama**: Install Ollama and pull the model: `ollama pull qwen2.5-coder:7b`.
- **Python 3.10+** & **Node.js**.

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🔄 Switching Back to Gemini

If you want to move from the local Ollama model to Google's Gemini API:

1. **Set API Key**: In `backend/app/config.py`, set your `GEMINI_API_KEY`.
2. **Update Imports**: In every agent file in `backend/app/agents/`, replace `ollama_client` imports with `gemini_client`.
3. **Update Calls**: Replace all `ollama_client.generate(prompt)` calls with `gemini_client.generate(prompt)`.

*Note: Gemini models are more permissive with JSON, so you may be able to simplify the JSON repair logic in `react_agent.py`.*
