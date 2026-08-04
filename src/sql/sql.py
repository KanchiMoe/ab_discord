from datetime import datetime, timezone
import logging
import psycopg2
import uuid

from src.discord.commands.quit import quit

UUID = str(uuid.uuid4())
TIMESTAMP = datetime.now(timezone.utc)

def add_run(action: str):
    try:
        conn = psycopg2.connect()

    except Exception as e:
        err_msg = f"Could not connect to database: {e}"
        logging.critical(err_msg)
        quit()
        raise RuntimeError(err_msg)


    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO metadata_runs (_uuid, _timestamp, _action)
            VALUES (%s, %s, %s);
            """,
            (UUID, TIMESTAMP, action)
        )
        conn.commit()
    conn.close()

    return None

def get_member_data() -> list:
    # to do, make this better w/ add_run
    try:
        conn = psycopg2.connect()

    except Exception as e:
        err_msg = f"Could not connect to database: {e}"
        logging.critical(err_msg)
        quit()
        raise RuntimeError(err_msg)

    # get all IDs
    all_member_ids = []

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT member_id FROM members;
            """,
        )
        # results from db
        rows = cursor.fetchall()
        for row in rows:
            member_id = row[0]
            all_member_ids.append(member_id)

    logging.info(f"Entries in all_member_ids: {len(all_member_ids)}")

    return all_member_ids