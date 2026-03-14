import { useEffect, useState } from "react";
import { fetchFiles, saveFile } from "../api/workspaceApi";

export default function FileExplorer({ onSelect, refreshKey }: any) {

  const [files, setFiles] = useState<string[]>([]);

  const loadFiles = () => {
    fetchFiles().then(setFiles);
  };

  useEffect(() => {
    loadFiles();
  }, [refreshKey]);

  const createFile = async () => {

    const name = prompt("Enter file name");

    if (!name) return;

    await saveFile(`workspace/${name}`, "");

    loadFiles();
  };

  return (

    <div className="h-full bg-gray-900 text-white p-3">

      <div className="flex justify-between mb-3">

        <h2 className="text-sm font-bold">Files</h2>

        <button
          className="bg-blue-600 px-2 text-xs"
          onClick={createFile}
        >
          +
        </button>

      </div>

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