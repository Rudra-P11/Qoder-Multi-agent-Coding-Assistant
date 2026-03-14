import { useState, useEffect } from "react";
import { connectSocket } from "../websocket/socket";
import type { AgentEvent } from "../types/agentTypes";

export const useAgent = () => {

  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [workspaceEvents, setWorkspaceEvents] = useState<any[]>([]);

  useEffect(() => {

    const ws = connectSocket((data: AgentEvent) => {

      setEvents(prev => [...prev, data]);

      if (data.agent === "workspace") {
        setWorkspaceEvents(prev => [...prev, data]);
      }

    });

    return () => ws.close();

  }, []);

  return { events, workspaceEvents };
};