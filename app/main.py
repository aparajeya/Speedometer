from fastapi import FastAPI, WebSocket
import asyncio
import threading

from app.ws_manager import ConnectionManager
from app.pg_listener import listen_for_speed

app = FastAPI()
manager = ConnectionManager()

@app.on_event("startup")
def startup():
    loop = asyncio.get_event_loop()
    thread = threading.Thread(
        target=listen_for_speed,
        args=(loop, manager),
        daemon=True
    )
    thread.start()

@app.websocket("/ws/speed")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except:
        manager.disconnect(websocket)

@app.get("/")
def health():
    return {"status": "YOGESH"}
