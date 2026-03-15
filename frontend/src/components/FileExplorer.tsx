import { useEffect, useState } from "react";
import { fetchFiles, saveFile, deleteFile } from "../api/workspaceApi";

export default function FileExplorer({ onSelect, onDelete, refreshKey }: any) {

  const [files, setFiles] = useState<string[]>([]);

  const loadFiles = () => {
    fetchFiles().then(setFiles);
  };

  useEffect(() => {
    loadFiles();
  }, [refreshKey]);

  const createFile = async () => {

    const name = prompt("Enter file name (e.g. main.cpp)");

    if (!name) return;

    // No prefix — file goes directly into root workspace
    await saveFile(name, "");

    loadFiles();
  };

  const handleDelete = async (e: React.MouseEvent, file: string) => {
    e.stopPropagation(); // prevent opening the file when clicking delete
    if (!confirm(`Delete "${file}"?`)) return;
    await deleteFile(file);
    if (onDelete) onDelete(file);
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
          className="flex items-center justify-between text-sm p-1 hover:bg-gray-700 cursor-pointer group"
        >
          <span className="flex-1 truncate" onClick={() => onSelect(file)}>
            {file}
          </span>
          <button
            title="Delete file"
            className="ml-1 text-red-400 opacity-0 group-hover:opacity-100 text-xs hover:text-red-300"
            onClick={(e) => handleDelete(e, file)}
          >
            🗑️
          </button>
        </div>

      ))}

    </div>
  );
}