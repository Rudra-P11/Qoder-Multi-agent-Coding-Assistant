export const connectSocket = (onMessage: any) => {

  const ws = new WebSocket("ws://localhost:8000/ws");

  ws.onopen = () => {
    console.log("WebSocket connected");

    ws.send(JSON.stringify({ type: "ping" }));
  };

  ws.onmessage = (event) => {

    const data = JSON.parse(event.data);

    onMessage(data);
  };

  ws.onerror = (error) => {

    console.error("WebSocket error:", error);

  };

  ws.onclose = () => {

    console.log("WebSocket closed");

  };

  return ws;
};