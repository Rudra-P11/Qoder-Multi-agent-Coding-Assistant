import { useState } from "react";
import { createTask } from "../api/agentApi";

export default function TaskInput({ onPlan }: any) {

  const [prompt, setPrompt] = useState("");

  const handleSubmit = async () => {

    const data = await createTask(prompt);

    onPlan(data);

  };

  return (

    <div className="p-4">

      <textarea
        className="w-full border p-2"
        placeholder="Enter coding task..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <button
        onClick={handleSubmit}
        className="mt-2 bg-blue-500 text-white px-4 py-2"
      >
        Run Agent
      </button>

    </div>
  );
}