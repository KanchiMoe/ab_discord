from datetime import datetime, timezone
import logging
import psycopg2
import uuid

UUID = str(uuid.uuid4())
TIMESTAMP = datetime.now(timezone.utc)

def add_run():
    try:
        conn = psycopg2.connect()

    except Exception as e:
        err_msg = f"Could not connect to database: {e}"
        logging.critical(err_msg)
        raise RuntimeError(err_msg)


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
