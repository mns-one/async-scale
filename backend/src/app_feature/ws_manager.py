# service.py
import asyncio
import json
from datetime import datetime, timezone
from fastapi import WebSocket

class StreamHub:
    def __init__(self):
        self.clients: dict[str, WebSocket] = {}
        self.seq = 0

    async def connect(self, client_id: str, ws: WebSocket):
        await ws.accept()
        self.clients[client_id] = ws
    
    def is_connected(self, client_id: str):   
        return client_id in self.clients

    def disconnect(self, client_id: str):
        self.clients.pop(client_id, None)

    async def broadcast(self, msg: str):
        self.seq += 1
        packet = {
            "payload": msg,
            "ts": datetime.now(timezone.utc).isoformat(),
            "seq": self.seq,
        }
        raw = json.dumps(packet)

        dead = []
        for cid, ws in self.clients.items():
            try:
                await ws.send_text(raw)
            except Exception:
                dead.append(cid)
        for cid in dead:
            self.disconnect(cid) 

hub = StreamHub()
