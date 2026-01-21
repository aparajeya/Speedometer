import time
import random
import psycopg2
from datetime import datetime, timezone
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/appdb"
)

def main():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    # 1. Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_speed (
            time TIMESTAMPTZ NOT NULL,
            speed_kmh DOUBLE PRECISION NOT NULL
        );
    """)

    # 2. Convert to hypertable
    cur.execute("""
        SELECT create_hypertable(
            'vehicle_speed',
            'time',
            if_not_exists => TRUE
        );
    """)

    print("🚀 Started inserting speed data every 1 second...")

    try:
        while True:
            speed = round(random.uniform(20, 120), 2)  # km/h
            now = datetime.now(timezone.utc)

            cur.execute(
                "INSERT INTO vehicle_speed (time, speed_kmh) VALUES (%s, %s)",
                (now, speed)
            )

            print(f"{now.isoformat()} | Speed: {speed} km/h")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()

