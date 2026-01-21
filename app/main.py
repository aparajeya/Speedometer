from fastapi import FastAPI, WebSocket, APIRouter
import asyncio
import threading

from app.ws_manager import ConnectionManager
from listener.pg_listener import listen_for_speed

from sqlalchemy import text
from enum import Enum

from db.db import engine

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
            await websocket.receive()#_text()  # keep alive
    except:
        manager.disconnect(websocket)

@app.get("/")
def health():
    return {"status": "YOGESH"}


def window_to_interval(window):
    return {
        "15m": "15 minutes",
        "1d": "1 day",
        "7d": "7 days",
    }[window.value]

class TimeWindow(str, Enum):
    last_15_min = "15m"
    last_1_day = "1d"
    last_7_days = "7d"

@app.get("/average-speed")
def average_speed(window: TimeWindow):
    interval = window_to_interval(window)

    query = text(f"""
        SELECT
            COALESCE(ROUND(AVG(speed_kmh)::numeric, 2), 0) AS avg_speed
        FROM vehicle_speed
        WHERE time >= now() - INTERVAL '{interval}';
    """)

    with engine.connect() as conn:
        result = conn.execute(query).fetchone()

    return {
        "window": window.value,
        "average_speed_kmh": float(result.avg_speed),
    }
