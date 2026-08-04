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

def sql_get_member_data() -> list:
    # to do, make this better w/ add_run
    try:
        conn = psycopg2.connect()

    except Exception as e:
        err_msg = f"Could not connect to database: {e}"
        logging.critical(err_msg)
        quit()
        raise RuntimeError(err_msg)

    all_member_ids    = []
    ids_not_in_server = []
    ids_in_server     = []

    # all IDs
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT member_id FROM members;
            """,
        )
        rows = cursor.fetchall()
        for row in rows:
            member_id = row[0]
            all_member_ids.append(member_id)
    logging.info(f"No of entries in all_member_ids: {len(all_member_ids)}")

    # NOT in server
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT member_id FROM members
            WHERE in_server = False;
            """,
        )
        rows = cursor.fetchall()
        for row in rows:
            ids_not_in_server.append(row[0])
    logging.info(f"No of entries in ids_not_in_server: {len(ids_not_in_server)}")

    # IN server
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT member_id FROM members
            WHERE in_server = True;
            """,
        )
        rows = cursor.fetchall()
        for row in rows:
            ids_in_server.append(row[0])
    logging.info(f"No of entries in ids_in_server: {len(ids_in_server)}")


    return all_member_ids, ids_not_in_server, ids_in_server
