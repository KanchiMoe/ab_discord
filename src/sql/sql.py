from datetime import datetime, timezone
import psycopg2
import uuid

UUID = str(uuid.uuid4())
TIMESTAMP = datetime.now(timezone.utc)

def add_run():
    conn = psycopg2.connect()

    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO metadata_runs (_uuid, _timestamp)
            VALUES (%s, %s);
            """,
            (UUID, TIMESTAMP)
        )
        conn.commit()
    conn.close()

    return None
