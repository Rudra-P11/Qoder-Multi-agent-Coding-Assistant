import { useState } from "react";

export default function FileExplorer() {

  const [files] = useState([
    "main.py",
    "utils.py",
    "data.csv"
  ]);

  return (

    <div className="h-full bg-gray-900 text-white p-3">

      <h2 className="text-sm font-bold mb-3">Files</h2>

      {files.map((file, i) => (

        <div
          key={i}
          className="text-sm p-1 hover:bg-gray-700 cursor-pointer"
        >
          {file}
        </div>

      ))}

    </div>

  );
}