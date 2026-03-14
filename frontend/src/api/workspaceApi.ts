import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const fetchFiles = async () => {

  const res = await API.get("/workspace/files");

  return res.data.files;

};

export const readFile = async (path: string) => {

  const res = await API.get("/workspace/file", {
    params: { path },
  });

  return res.data.content;

};

export const saveFile = async (path: string, content: string) => {

  await API.post("/workspace/file", null, {
    params: { path, content },
  });

};