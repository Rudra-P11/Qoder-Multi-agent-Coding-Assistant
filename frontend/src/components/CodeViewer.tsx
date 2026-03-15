import Editor from "@monaco-editor/react";

type Props = {
  filename: string;
  code: string;
  onChange: (value: string) => void;
  onRun: () => void;
};

export default function CodeViewer({ filename, code, onChange, onRun }: Props) {

  // Derive language from extension
  const getLanguage = (name: string) => {
    if (name.endsWith(".py")) return "python";
    if (name.endsWith(".js")) return "javascript";
    if (name.endsWith(".ts") || name.endsWith(".tsx")) return "typescript";
    if (name.endsWith(".cpp") || name.endsWith(".c")) return "cpp";
    if (name.endsWith(".java")) return "java";
    if (name.endsWith(".json")) return "json";
    if (name.endsWith(".md")) return "markdown";
    return "plaintext";
  };

  const currentLanguage = getLanguage(filename);

  return (
    <div className="flex flex-col h-full bg-[#1e1e1e]">
      <div className="flex justify-between items-center p-2 bg-gray-800 text-white text-sm border-b border-gray-700">
        <span>{filename || "No file selected"}</span>
        <button 
          onClick={onRun}
          disabled={!filename}
          className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-xs disabled:opacity-50"
        >
          Run Code
        </button>
      </div>
      <div className="flex-1">
        <Editor
          height="100%"
          language={currentLanguage}
          theme="vs-dark"
          value={code}
          onChange={(value) => onChange(value || "")}
          options={{
            fontSize: 14,
            minimap: { enabled: false },
            automaticLayout: true
          }}
        />
      </div>
    </div>
  );
}