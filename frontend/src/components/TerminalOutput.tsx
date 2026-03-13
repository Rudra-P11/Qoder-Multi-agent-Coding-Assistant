export default function TerminalOutput({ logs }: { logs: string[] }) {

  return (

    <div className="bg-black text-green-400 h-full overflow-auto p-3 text-sm font-mono">

      {logs.map((log, i) => (

        <div key={i}>{log}</div>

      ))}

    </div>

  );
}