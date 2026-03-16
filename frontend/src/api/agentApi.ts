import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const createTask = async (prompt: string) => {
  const res = await API.post("/task", { prompt });
  return res.data;
};

export const approvePlan = async (sessionId: string) => {
  const res = await API.post("/approve-plan", {
    session_id: sessionId,
    approved: true
  });
  return res.data;
};

export const submitClarification = async (sessionId: string, answers: Record<string, string>) => {
  const res = await API.post("/task/clarify", {
    session_id: sessionId,
    answers
  });
  return res.data;
};

export const submitEscalation = async (sessionId: string, choice: "replan" | "simplify" | "pause") => {
  const res = await API.post("/task/escalate", {
    session_id: sessionId,
    choice
  });
  return res.data;
};