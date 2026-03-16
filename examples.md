# Qoder: Example Task Scenarios

This document showcases 3 distinct scenarios where Qoder demonstrates its self-correction, logic, and novel ambiguity handling.

---

## 1. The "Broken Logic" Self-Correction
**Scenario**: The user asks the agent to create a script that calculates the factorial of a number, but provide a task where the agent might introduce a common bug (e.g., using a non-integer or negative number).

**Prompt**: *"Write a python script called factorial.py that takes a number and prints its factorial. Then run it with input 5."*

**The Loop**:
1.  **Action**: Agent writes `factorial.py`.
2.  **Mistake**: The agent forget to handle the recursive base case correctly or makes a syntax error.
3.  **Execution**: `run_code("factorial.py")` fails with `SyntaxError` or `RecursionError`.
4.  **Self-Correction**: The ReAct agent reads the `stderr`, identifies the line with the error, reasons about the fix, and rewrites the file correctly.
5.  **Success**: The second execution succeeds.

---

## 2. The "Silent Assumption" Ambiguity Check
**Scenario**: The user gives a vague prompt that could lead to multiple implementations.

**Prompt**: *"I want a script to analyze a dataset of sales."*

**The Detection**:
1.  **Ambiguity Analyzer**: Detects high ambiguity (Score: 0.82). Missing info: What is the input format (CSV? JSON?)? What analysis is needed (Sum? Average? Trends?)? What output is expected?
2.  **Clarification**: The UI interrupts the flow and asks:
    - *Q1: What is the format of the sales data? (Options: CSV, JSON, Agent decides)*
    - *Q2: What metric do you want to calculate? (Options: Total Revenue, Average Order Value, Agent decides)*
3.  **User Response**: User selects "CSV" and "Total Revenue".
4.  **Execution**: The planner creates a plan specifically for CSV revenue calculation, avoiding the frustration of a generic analysis script that may not have worked for the user's specific data.

---

## 3. The "Stuck Loop" Escalation
**Scenario**: The agent is asked to fetch data from an API that requires an API key, but the key is not provided.

**Prompt**: *"Write a script to get the latest weather for New York and save it to weather.txt. Use the OpenWeatherMap API."*

**The Dead-End**:
1.  **Action**: Agent writes the code without an API key.
2.  **Execution**: Fails with `401 Unauthorized`.
3.  **Retry**: Agent tries to "fix" the URL or headers. Fails again.
4.  **Repeat**: Agent gets stuck in a loop of trying small code changes.
5.  **Escalation**: After the 3rd failed attempt in the `run_code` block, the **Escalation Panel** pops up.
    - *Message: "I'm stuck. The API returns 401 Unauthorized. I need a valid API key."*
6.  **Resolution**: User chooses "Simplify the task" or "Pause". This prevents the agent from infinitely burning local compute or hitting API rate limits fruitlessly.
