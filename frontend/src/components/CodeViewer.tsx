import Editor from "@monaco-editor/react";
import * as monaco from "monaco-editor";

export default function CodeViewer({ code }: { code: string }) {

  return (
    <div className="h-full w-full">
      <Editor
        height="100%"
        defaultLanguage="javascript"
        theme="vs-dark"
        value={code}
        beforeMount={(m) => {
          Object.assign(m, monaco);
        }}
        options={{
          fontSize: 14,
          minimap: { enabled: false },
          automaticLayout: true,
        }}
      />
    </div>
  );
}