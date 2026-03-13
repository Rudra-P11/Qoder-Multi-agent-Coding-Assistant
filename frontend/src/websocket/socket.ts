export const connectSocket = (onMessage: any) => {

  const ws = new WebSocket("ws://localhost:8000/ws");

  ws.onmessage = (event) => {

    const data = JSON.parse(event.data);

    onMessage(data);
  };

  return ws;
};