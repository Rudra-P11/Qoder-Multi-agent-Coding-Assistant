import { useState } from "react";
import { createTask } from "../api/agentApi";

type Props = {
  onPlan?: (data: any) => void;
};

export default function TaskInput({ onPlan }: Props) {

  const [prompt, setPrompt] = useState("");

  const handleSubmit = async () => {

    if (!prompt.trim()) return;

    const data = await createTask(prompt);

    if (onPlan) {
      onPlan(data);
    }

    setPrompt("");
  };

  return (

    <div className="bg-gray-900 p-3 flex gap-2">

      <input
        className="flex-1 bg-gray-800 text-white p-2 rounded"
        placeholder="Ask Qoder to build something..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white px-4 rounded"
      >
        Run
      </button>

    </div>
  );
}