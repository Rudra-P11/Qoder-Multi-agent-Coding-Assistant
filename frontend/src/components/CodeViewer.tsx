import Editor from "@monaco-editor/react";

export default function CodeViewer({ code }: any) {

  return (

    <Editor
      height="500px"
      defaultLanguage="python"
      value={code}
      theme="vs-dark"
    />

  );
}