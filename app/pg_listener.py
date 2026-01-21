import psycopg2
import select
import os
import asyncio
import json

DATABASE_URL = os.getenv("DATABASE_URL")

def listen_for_speed(loop, manager):
    conn = psycopg2.connect(DATABASE_URL)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()
    cur.execute("LISTEN vehicle_speed_channel;")
    print("👂 Listening for vehicle_speed notifications...")

    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            continue
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            payload = notify.payload

            # Send to websocket clients
            asyncio.run_coroutine_threadsafe(
                manager.broadcast(payload),
                loop
            )

