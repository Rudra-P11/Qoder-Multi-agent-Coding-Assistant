import Editor from "@monaco-editor/react";

type Props = {
  code: string;
  onChange: (value: string) => void;
};

export default function CodeViewer({ code, onChange }: Props) {

  return (
    <Editor
      height="100%"
      defaultLanguage="javascript"
      theme="vs-dark"
      value={code}
      onChange={(value) => onChange(value || "")}
      options={{
        fontSize: 14,
        minimap: { enabled: false },
        automaticLayout: true
      }}
    />
  );
}