import { useState, useEffect } from "react";

import FileExplorer from "../components/FileExplorer";
import CodeViewer from "../components/CodeViewer";
import TerminalOutput from "../components/TerminalOutput";
import AgentTimeline from "../components/AgentTimeline";
import TaskInput from "../components/TaskInput";

import { useAgent } from "../hooks/useAgent";
import { readFile, saveFile } from "../api/workspaceApi";

export default function IDEPage() {

  const { events, workspaceEvents } = useAgent();

  const [code, setCode] = useState("");
  const [currentFile, setCurrentFile] = useState("");
  const [refreshKey, setRefreshKey] = useState(0);

  const openFile = async (path: string) => {

    const content = await readFile(path);

    setCurrentFile(path);
    setCode(content);

  };

  const saveCurrentFile = async () => {

    if (!currentFile) return;

    await saveFile(currentFile, code);

  };

  useEffect(() => {

    if (workspaceEvents.length > 0) {
      setRefreshKey(prev => prev + 1);
    }

  }, [workspaceEvents]);

  const terminalLogs = events.map(
    (e) => `${e.agent}: ${e.message}`
  );

  return (

    <div className="h-screen flex flex-col">

      <div className="flex flex-1 overflow-hidden">

        <div className="w-48 border-r border-gray-700">
          <FileExplorer onSelect={openFile} refreshKey={refreshKey} />
        </div>

        <div className="flex-1 border-r border-gray-700">
          <CodeViewer code={code} onChange={setCode} />
        </div>

        <div className="w-72 bg-gray-900 text-white">
          <AgentTimeline events={events} />
        </div>

      </div>

      <div className="h-40 border-t border-gray-700">
        <TerminalOutput logs={terminalLogs} />
      </div>

      <div className="flex">

        <TaskInput />

        <button
          onClick={saveCurrentFile}
          className="bg-green-600 text-white px-4"
        >
          Save
        </button>

      </div>

    </div>
  );
}