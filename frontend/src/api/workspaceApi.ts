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

export const runCode = async (path: string) => {

  const res = await API.post("/workspace/run", null, {
    params: { path },
  });

  return res.data;

};

export const deleteFile = async (path: string) => {

  await API.delete("/workspace/file", {
    params: { path },
  });

};