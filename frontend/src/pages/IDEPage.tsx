import TaskInput from "../components/TaskInput";
import AgentTimeline from "../components/AgentTimeline";
import { useAgent } from "../hooks/useAgent";

export default function IDEPage() {

  const { events } = useAgent();

  return (

    <div className="grid grid-cols-3 h-screen">

      <div className="border-r">

        <TaskInput />

      </div>

      <div className="border-r">

        <h2 className="p-2 font-bold">Code</h2>

      </div>

      <div>

        <AgentTimeline events={events} />

      </div>

    </div>

  );
}