import logging

from src.constants import AB_SERVER_ID, RANK_ROLE_IDS, RANK_EXCEMPTION_ROLE_IDS, RANK_LOG_CHANNEL
from src.discord.bot import DiscordBot

async def no_access_rank_check():
    # discord setup
    discord_bot = DiscordBot.instance
    guild = discord_bot.get_guild(AB_SERVER_ID)

    users_without_ranks = []

    for member in guild.members:
        for role in member.roles:
            if role.id in RANK_EXCEMPTION_ROLE_IDS:
                break
            if role.id in RANK_ROLE_IDS:
                break
        else:
            users_without_ranks.append(member.id)
    
    # get log channel (cache)
    channel = guild.get_thread(RANK_LOG_CHANNEL)

    # if not in cache
    if channel is None:
        logging.warning("Channel was not found in cache")

        channel = await guild.fetch_channel(RANK_LOG_CHANNEL)

    # send message
    logging.info(f"{len(users_without_ranks)} users without at least one access rank")
    await channel.send(content=f"There are **{len(users_without_ranks)}** users without at least one access rank.")

    return
