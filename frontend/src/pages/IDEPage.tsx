import { useState, useEffect } from "react";

import FileExplorer from "../components/FileExplorer";
import CodeViewer from "../components/CodeViewer";
import TerminalOutput from "../components/TerminalOutput";
import AgentTimeline from "../components/AgentTimeline";
import TaskInput from "../components/TaskInput";
import PlanPanel from "../components/PlanPanel";
import ClarificationPanel from "../components/ClarificationPanel";
import EscalationPanel from "../components/EscalationPanel";

import { useAgent } from "../hooks/useAgent";
import { createTask, approvePlan, submitClarification, submitEscalation } from "../api/agentApi";
import { readFile, saveFile, runCode } from "../api/workspaceApi";

interface ClarificationState {
  sessionId: string;
  ambiguityScore: number;
  questions: { id: string; question: string; options: string[] }[];
}

interface EscalationState {
  sessionId: string;
  attempts: number;
  lastError: string;
}

export default function IDEPage() {
  const { events, workspaceEvents } = useAgent();

  const [code, setCode] = useState("");
  const [currentFile, setCurrentFile] = useState("");
  const [plan, setPlan] = useState<string[]>([]);
  const [sessionId, setSessionId] = useState("");
  const [localLogs, setLocalLogs] = useState<string[]>([]);

  // New feature states
  const [clarification, setClarification] = useState<ClarificationState | null>(null);
  const [escalation, setEscalation] = useState<EscalationState | null>(null);

  // Auto-save debounce effect
  useEffect(() => {
    if (!currentFile) return;
    const timeoutId = setTimeout(() => { saveFile(currentFile, code); }, 1000);
    return () => clearTimeout(timeoutId);
  }, [code, currentFile]);

  // Auto-open files written by the agent
  useEffect(() => {
    if (workspaceEvents.length === 0) return;
    const latest = workspaceEvents[workspaceEvents.length - 1];
    if (latest?.message === "file_updated" && latest?.data?.path) {
      openFile(latest.data.path);
    }
  }, [workspaceEvents]);

  // Listen for ambiguity and escalation WebSocket events
  useEffect(() => {
    if (events.length === 0) return;
    const latest = events[events.length - 1];

    if (latest?.agent === "ambiguity" && latest?.message === "Task needs clarification" && latest?.data) {
      setClarification({
        sessionId: latest.data.session_id,
        ambiguityScore: latest.data.score,
        questions: latest.data.questions
      });
    }

    if (latest?.agent === "escalation" && latest?.data) {
      setEscalation({
        sessionId: latest.data.session_id,
        attempts: latest.data.attempts,
        lastError: latest.data.last_error || "Unknown error"
      });
    }
  }, [events]);

  const openFile = async (path: string) => {
    if (path === currentFile) return;
    if (currentFile && code) await saveFile(currentFile, code);
    const content = await readFile(path);
    setCurrentFile(path);
    setCode(content);
  };

  const handleRunCode = async () => {
    if (!currentFile) return;
    await saveFile(currentFile, code);
    setLocalLogs(prev => [...prev, `[USER] Running ${currentFile}...`]);
    try {
      const result = await runCode(currentFile);
      if (result.stdout) setLocalLogs(prev => [...prev, `[STDOUT] ${result.stdout}`]);
      if (result.stderr) setLocalLogs(prev => [...prev, `[STDERR] ${result.stderr}`]);
      if (result.error) setLocalLogs(prev => [...prev, `[ERROR] ${result.error}`]);
      setLocalLogs(prev => [...prev, `[EXIT CODE] ${result.exit_code}`]);
    } catch (error: any) {
      setLocalLogs(prev => [...prev, `[ERROR] Failed to execute code: ${error.message}`]);
    }
  };

  const handlePrompt = async (prompt: string) => {
    setClarification(null);
    setEscalation(null);
    setLocalLogs(prev => [...prev, `[SYSTEM] Sending task to planner...`]);
    try {
      const data = await createTask(prompt);
      setSessionId(data.session_id);
      if (data.needs_clarification) {
        // Don't set plan yet — wait for clarification
        setClarification({
          sessionId: data.session_id,
          ambiguityScore: data.ambiguity_score,
          questions: data.questions
        });
      } else {
        setPlan(data.plan || []);
      }
    } catch (error: any) {
      const msg = error?.response?.data?.detail || error?.response?.data?.error || error?.message || "Unknown error";
      setLocalLogs(prev => [...prev, `[SYSTEM ERROR] Planner failed: ${msg}`]);
    }
  };

  const handleClarificationSubmit = async (answers: Record<string, string>) => {
    if (!clarification) return;
    setClarification(null);
    setLocalLogs(prev => [...prev, `[SYSTEM] Clarification submitted. Planning with constraints...`]);
    try {
      const data = await submitClarification(clarification.sessionId, answers);
      setPlan(data.plan || []);
    } catch (error: any) {
      const msg = error?.response?.data?.error || error?.message || "Unknown error";
      setLocalLogs(prev => [...prev, `[SYSTEM ERROR] Clarification failed: ${msg}`]);
    }
  };

  const handleClarificationSkip = async () => {
    if (!clarification) return;
    const skippedAnswers: Record<string, string> = {};
    clarification.questions.forEach(q => { skippedAnswers[q.id] = "Agent decides"; });
    await handleClarificationSubmit(skippedAnswers);
  };

  const handleApprove = async () => {
    try {
      await approvePlan(sessionId);
    } catch (error: any) {
      const msg = error?.response?.data?.error || error?.message || "Unknown error";
      setLocalLogs(prev => [...prev, `[SYSTEM ERROR] Approval failed: ${msg}`]);
    }
    setPlan([]);
  };

  const handleEscalation = async (choice: "replan" | "simplify" | "pause") => {
    if (!escalation) return;
    setEscalation(null);
    setLocalLogs(prev => [...prev, `[SYSTEM] Escalation choice: ${choice}`]);
    try {
      await submitEscalation(escalation.sessionId, choice);
    } catch (error: any) {
      const msg = error?.response?.data?.error || error?.message || "Unknown error";
      setLocalLogs(prev => [...prev, `[SYSTEM ERROR] Escalation failed: ${msg}`]);
    }
  };

  const handleFileDeleted = (file: string) => {
    if (currentFile === file) { setCurrentFile(""); setCode(""); }
  };

  const agentLogs = events.flatMap((e) => {
    if (e.message.startsWith("Attempt ")) {
      const logs = [
        `\n======================================================`,
        `[EXECUTION] ${e.message}`,
        `======================================================`
      ];
      if (e.data) {
        if (e.data.task) { logs.push(`--- TASK INPUT ---`); logs.push(e.data.task); }
        if (e.data.code) { logs.push(`--- GENERATED CODE ---`); logs.push(e.data.code); }
        let hasOutput = false;
        if (e.data.result) {
          logs.push(`--- EXECUTION OUTPUT ---`);
          if (e.data.result.stdout) { logs.push(`[STDOUT]\n${e.data.result.stdout}`); hasOutput = true; }
          if (e.data.result.stderr) { logs.push(`[STDERR]\n${e.data.result.stderr}`); hasOutput = true; }
          if (e.data.result.error) { logs.push(`[ERROR]\n${e.data.result.error}`); hasOutput = true; }
          if (!hasOutput) logs.push(`[NO OUTPUT]`);
          logs.push(`--- FINAL RESULT ---`);
          logs.push(`Exit Code: ${e.data.result.exit_code !== undefined ? e.data.result.exit_code : "N/A"}`);
        }
      }
      logs.push(`======================================================\n`);
      return logs;
    }

    const logs = [`${e.agent}: ${e.message}`];
    if (e.data) {
      if (e.data.stdout) logs.push(`> [STDOUT] ${e.data.stdout}`);
      if (e.data.stderr) logs.push(`> [STDERR] ${e.data.stderr}`);
      if (e.data.error) logs.push(`> [ERROR] ${e.data.error}`);
      if (e.data.exit_code !== undefined && !e.message.startsWith("Attempt ")) logs.push(`> [EXIT CODE] ${e.data.exit_code}`);
    }
    return logs;
  });

  const terminalLogs = [...localLogs, ...agentLogs];

  return (
    <div className="h-screen flex flex-col">

      {/* Clarification panel — shown instead of plan when task is ambiguous */}
      {clarification && (
        <ClarificationPanel
          sessionId={clarification.sessionId}
          ambiguityScore={clarification.ambiguityScore}
          questions={clarification.questions}
          onSubmit={handleClarificationSubmit}
          onSkip={handleClarificationSkip}
        />
      )}

      {plan.length > 0 && !clarification && (
        <PlanPanel plan={plan} onApprove={handleApprove} />
      )}

      {/* Escalation panel — shown inline when agent is stuck */}
      {escalation && (
        <div style={{ position: "fixed", bottom: "120px", right: "16px", width: "380px", zIndex: 50 }}>
          <EscalationPanel
            sessionId={escalation.sessionId}
            attempts={escalation.attempts}
            lastError={escalation.lastError}
            onChoice={handleEscalation}
          />
        </div>
      )}

      <div className="flex flex-1 overflow-hidden">
        <div className="w-48 border-r border-gray-700">
          <FileExplorer onSelect={openFile} onDelete={handleFileDeleted} refreshKey={workspaceEvents.length} />
        </div>

        <div className="flex-1 border-r border-gray-700">
          <CodeViewer
            filename={currentFile}
            code={code}
            onChange={setCode}
            onRun={handleRunCode}
          />
        </div>

        <div className="w-72 bg-gray-900 text-white">
          <AgentTimeline events={events} />
        </div>
      </div>

      <div className="h-40 border-t border-gray-700 overflow-y-auto">
        <TerminalOutput logs={terminalLogs} />
      </div>

      <TaskInput onPrompt={handlePrompt} />

    </div>
  );
}