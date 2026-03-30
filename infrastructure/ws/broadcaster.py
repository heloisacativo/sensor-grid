from fastapi import WebSocket
from typing import Set

active_websockets: Set[WebSocket] = set()

async def broadcast_event(evento: dict):
    if not active_websockets:
        return

    stale = []
    for websocket in active_websockets:
        try:
            await websocket.send_json({"type": "new_event", "event": evento})
        except Exception:
            stale.append(websocket)

    for websocket in stale:
        active_websockets.discard(websocket)
