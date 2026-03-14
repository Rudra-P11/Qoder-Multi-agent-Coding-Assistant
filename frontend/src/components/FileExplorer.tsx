import { useEffect, useState } from "react";
import { fetchFiles } from "../api/workspaceApi";

export default function FileExplorer({ onSelect, refreshKey }: any) {

  const [files, setFiles] = useState<string[]>([]);

  const loadFiles = () => {
    fetchFiles().then(setFiles);
  };

  useEffect(() => {
    loadFiles();
  }, [refreshKey]);

  return (

    <div className="h-full bg-gray-900 text-white p-3">

      <h2 className="text-sm font-bold mb-3">Files</h2>

      {files.map((file, i) => (

        <div
          key={i}
          className="text-sm p-1 hover:bg-gray-700 cursor-pointer"
          onClick={() => onSelect(file)}
        >
          {file}
        </div>

      ))}

    </div>
  );
}