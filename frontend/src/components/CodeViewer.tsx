import Editor from "@monaco-editor/react";

export default function CodeViewer({ code }: { code: string }) {

  return (

    <div className="h-full">

      <Editor
        height="100%"
        defaultLanguage="python"
        theme="vs-dark"
        value={code}
        options={{
          fontSize: 14,
          minimap: { enabled: false },
          automaticLayout: true
        }}
      />

    </div>

  );
}