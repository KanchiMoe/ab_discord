import logging

from src.constants import AB_SERVER_ID
from src.discord.bot import DiscordBot
from src.sql.sql import sql_get_member_data, sql_add_new_member, sql_member_returned, sql_member_left

async def memberlist():
    # discord setup
    discord_bot = DiscordBot.instance
    guild = discord_bot.get_guild(AB_SERVER_ID)
    if not guild:
        err_msg = f"Could not get server {AB_SERVER_ID}"
        logging.critical(err_msg)
        raise RuntimeError(err_msg)

    db_all_member_ids, db_not_in_server_ids, db_in_server_ids = sql_get_member_data()
    
    current_guild_member_ids = set()
    for member in guild.members:
        current_guild_member_ids.add(member.id)

        # while we're looping through each server member...

        # ID not in db = new user
        if member.id not in db_all_member_ids:
            sql_add_new_member(member)
            logging.info(f"Member {member.name} ({member.id}) has joined the server")
            continue

        # member in server, but marked as not in server = user returned
        elif member.id in db_not_in_server_ids:
            sql_member_returned(member)
            logging.info(f"Member {member.name} ({member.id}) has rejoined the server")
            continue

        else:
            continue

    # not in member list, but marked as in server = member left server
    db_ids_marked_in_server = set()
    for member_id in db_in_server_ids:
        db_ids_marked_in_server.add(member_id)

    left_but_marked_in_server = db_ids_marked_in_server - current_guild_member_ids
    for member_id in left_but_marked_in_server:
        sql_member_left(member_id)
        logging.info(f"Member {member_id} has left the server")
