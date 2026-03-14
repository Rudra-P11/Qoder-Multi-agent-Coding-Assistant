import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const createTask = async (prompt: string) => {

  const res = await API.post("/task", { prompt });

  return res.data;

};

export const approvePlan = async (sessionId: string) => {

  await API.post("/approve-plan", null, {
    params: { session_id: sessionId },
  });

};