import logging

from src.constants import AB_SERVER_ID, COLOUR_ROLES, COLOUR_LOG_CHANNEL
from src.discord.bot import DiscordBot

import time
import random

async def no_colour_check():

    # discord setup
    discord_bot = DiscordBot.instance
    guild = discord_bot.get_guild(AB_SERVER_ID)

    # check each role exists first
    for role in COLOUR_ROLES:
        checked_role = guild.get_role(role)

        if checked_role is None:
            logging.error(f"Role ID {role} does not exist")
            raise ValueError
                
    logging.info("All colour roles exist")
    
    # store
    users_without_colour_roles = []

    # for each member
    for member in guild.members:
        
        # if they have a role in the colour list
        for role in member.roles:
            if role.id in COLOUR_ROLES:
                break # escape role in roles loop

            if role.id == 933261741746446376: # NPC
                break # escape role in roles loop
        
        # if dont have a role 
        else:
            users_without_colour_roles.append(member.id)

    # get log channel (cache)
    channel = guild.get_thread(COLOUR_LOG_CHANNEL)

    # if not in cache
    if channel is None:
        logging.warning("Channel was not found in cache")
        channel = await guild.fetch_channel(COLOUR_LOG_CHANNEL)

    # send message
    await channel.send(content=f"There are **{len(users_without_colour_roles)}** users without a role colour role.")

    # assign a random role
    for member in users_without_colour_roles:

        random_role_id = random.choice(COLOUR_ROLES)
        random_role    = guild.get_role(random_role_id)

        try:
            user = await guild.fetch_member(member)

            await user.add_roles(random_role)
            logging.info(f"{random_role.name} was assigned to {user.name} ({user.id})")
            await channel.send(content=f"**{random_role.name}** was assigned to {user.mention}")

            # to not flood discord
            time.sleep(3)
            
        except Exception as e:
            print(e)


