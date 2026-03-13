import { useState } from "react";

import FileExplorer from "../components/FileExplorer";
import CodeViewer from "../components/CodeViewer";
import TerminalOutput from "../components/TerminalOutput";
import AgentTimeline from "../components/AgentTimeline";
import TaskInput from "../components/TaskInput";

import { useAgent } from "../hooks/useAgent";

export default function IDEPage() {

  const { events } = useAgent();

  const [code, setCode] = useState("// Agent generated code will appear here");

  const terminalLogs = events.map(
    (e) => `${e.agent}: ${e.message}`
  );

  const handlePlan = (data: any) => {
    console.log("Plan received:", data);
  };

  return (

    <div className="h-screen flex flex-col">

      <div className="flex flex-1 overflow-hidden">

        {/* File Explorer */}
        <div className="w-48 border-r border-gray-700">
          <FileExplorer />
        </div>

        {/* Code Editor */}
        <div className="flex-1 border-r border-gray-700">
          <CodeViewer code={code} />
        </div>

        {/* Agent Timeline */}
        <div className="w-72 bg-gray-900 text-white">
          <AgentTimeline events={events} />
        </div>

      </div>

      {/* Terminal */}
      <div className="h-40 border-t border-gray-700">
        <TerminalOutput logs={terminalLogs} />
      </div>

      {/* Prompt */}
      <TaskInput onPlan={handlePlan} />

    </div>
  );
}