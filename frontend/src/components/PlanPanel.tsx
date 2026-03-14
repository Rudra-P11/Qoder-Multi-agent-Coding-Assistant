export default function PlanPanel({ plan, onApprove }: any) {

  return (

    <div className="bg-gray-900 text-white p-3 border-b border-gray-700">

      <h2 className="font-bold mb-2">Agent Plan</h2>

      <ul className="text-sm">

        {plan.map((step: string, i: number) => (
          <li key={i}>• {step}</li>
        ))}

      </ul>

      <button
        onClick={onApprove}
        className="mt-3 bg-green-600 px-4 py-1"
      >
        Approve Plan
      </button>

    </div>

  );
}