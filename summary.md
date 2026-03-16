# Project Overview: Agentic Coding Assistant

## 1. Multi-Agent Architecture and Planning
The core of the system is a modular backend where tasks are decomposed into structured execution plans. A **Task Interpreter** extracts technical metadata (language, libraries) to ground the assistant’s strategy. This leads into a **Planning Phase**, where a specialized agent generates a JSON array of discrete tasks. This "roadmap" is saved as a persistent To-Do list in the workspace, ensuring the agent can recover its state and maintain reliability even after a system crash.

## 2. Sandboxed Execution and Security
To meet strict security requirements, the assistant employs a robust workspace management system. Code execution occurs in an isolated Python subprocess restricted to a dedicated directory. Key safety features include:

* **Path Validation:** Logic that blocks "dot-dot-slash" directory traversal attacks.
* **Process Control:** A mandatory 30-second timeout to prevent infinite loops.
* **Feedback Capture:** The system captures `stdout`, `stderr`, and exit codes, transforming the LLM from a text generator into a functional software worker.

## 3. The Self-Correction Loop
A recursive agent loop handles errors by feeding `stderr` back into a **Debugger Agent**. To prevent the model from repeating failed logic, a **Reflector Agent** analyzes why a previous attempt failed before proposing a specific technical change for the next iteration. The system labels these iterations (e.g., Attempt 1, Attempt 2) to maintain a transparent history of the self-healing process.

## 4. Specialized Tools and Model Orchestration
The agent navigates its environment using a suite of tools, including `run_code`, `read_file`, `write_file`, and `todo_management`. A unique **Model Recommendation** feature optimizes performance by analyzing task complexity:

* **Local Models (e.g., Qwen2.5-Coder):** Suggested for simple, single-file scripts to reduce latency.
* **Cloud Models (e.g., Gemini):** Recommended for complex, multi-file refactoring and high-reasoning tasks.

## 5. User Interface and Ambiguity Analysis
The frontend is a **React-based web UI** featuring a live terminal and the **Monaco Editor**. It uses WebSockets to stream "Agent Thinking" states and real-time execution outputs. To handle underspecified prompts, the author implemented an **Ambiguity Analyzer**. It scores requests based on clarity and scope; if a prompt is too vague, the system interrupts the workflow to ask the user targeted, multiple-choice clarifying questions.

## 6. Technical Reflections and Resilience
The development process addressed several "real-world" AI hurdles:

* **The "Infinite Write" Bug:** Solved by forcing the agent to run code before it can edit the same file again.
* **JSON Parsing:** A "JSON Scavenger" utility was built to extract valid data from the prose-heavy outputs of smaller 7B models.
* **Context Awareness:** A "repo-map" allows the agent to search the workspace and reference its own previous modules, ensuring consistency in multi-file projects.

## 7. Memory and Context Handling
The assistant manages its "mental state" through a multi-tiered memory system:
* **Short-Term Memory:** Maintains a rolling conversation history within each agent's execution loop.
* **Persistent Working Memory:** Uses files like `project_todo.md` to store project-level state that persists across sessions.
* **Context Management:** Implements pruning and summarization logic to handle LLM token limits while retaining critical task instructions and previous success/failure results.

The final prototype is a self-contained, portable, and secure system that demonstrates a full software development lifecycle—moving from a vague user request to a verified, functional codebase through autonomous reasoning and human-in-the-loop clarification.