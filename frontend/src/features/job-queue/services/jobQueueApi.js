import { BASE_HTTP, BASE_WS } from "../constants";

export async function postSessionConfig({ clientId, size, interval_, target }) {
  return fetch(`${BASE_HTTP}/app-feature/data`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      client_id: clientId,
      size,
      interval: interval_,
      target,
    }),
  });
}

export function createSessionSocket(clientId) {
  return new WebSocket(`${BASE_WS}/app-feature/connect/${clientId}`);
}

