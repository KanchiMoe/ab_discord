from datetime import datetime, timezone
import logging
import psycopg2
import uuid

from discord import Member

class Database:
    # class vars
    _connection = None

    @classmethod
    def connect(cls):
        from src.discord.commands.quit import quit

        try:
            cls._connection = psycopg2.connect()
            logging.info("Connected to database")

        except Exception as e:
            err_msg = f"Could not connect to database: {e}"
            logging.critical(err_msg)
            quit()
            raise RuntimeError(err_msg)

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            raise RuntimeError("Database not connected. Call Database.connect() first.")
        return cls._connection

    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None
            logging.info("Database connection closed")


UUID = str(uuid.uuid4())
TIMESTAMP = datetime.now(timezone.utc)

def add_run(action: str):
    conn = Database.get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO metadata_runs (_uuid, _timestamp, _action)
            VALUES (%s, %s, %s);
            """,
            (UUID, TIMESTAMP, action)
        )
        conn.commit()

    return None

def sql_get_member_data() -> list:
    conn = Database.get_connection()

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

def sql_add_new_member(member: Member):
    conn = Database.get_connection()

    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO members
            (member_id, member_name, account_created, in_server, nickname, joined, is_bot)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (member.id, member.name, member.created_at, True, member.display_name, member.joined_at, member.bot)
        )
        logging.info(f"Member joined, rows updated: {cursor.rowcount}")
        conn.commit()

def sql_member_returned(member: Member):
    conn = Database.get_connection()

    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE members
            SET in_server = True
            WHERE member_id = %s AND in_server = False;
            """,
            (member.id,)
        )
        logging.info(f"Member rejoined, rows updated: {cursor.rowcount}")
        conn.commit()

def sql_member_left(member_id: int):
    conn = Database.get_connection()

    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE members
            SET in_server = False
            WHERE member_id = %s AND in_server = True;
            """,
            (member_id,)
        )
        logging.info(f"Member left, rows updated: {cursor.rowcount}")
        conn.commit()
