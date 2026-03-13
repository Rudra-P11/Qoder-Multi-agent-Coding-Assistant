import type { AgentEvent } from "../types/agentTypes";

export default function AgentTimeline({ events }: { events: AgentEvent[] }) {

  return (

    <div className="p-4 overflow-auto h-full">

      {events.map((e, i) => (

        <div key={i} className="mb-2 text-sm">

          <span className="font-bold text-blue-400">
            {e.agent}
          </span>

          <span className="ml-2 text-gray-300">
            {e.message}
          </span>

        </div>

      ))}

    </div>

  );
}