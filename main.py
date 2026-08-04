import asyncio
from dotenv import load_dotenv
import logging
import os
import sys

from src.discord.bot import DiscordBot
from src.discord.commands.quit import quit

if not os.environ.get("NOT_DOTENV"):
    load_dotenv()
    print(".env was loaded.")

DEFAULT_LOG_LEVEL = "INFO"
LOG_LEVEL = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)
if LOG_LEVEL not in logging._nameToLevel:
    raise RuntimeError(f"Invalid LOG_LEVEL={LOG_LEVEL}")

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=LOG_LEVEL
)

async def main(option: int, run_type: str):
    from src.sql.sql import Database, add_run
    from src.discord.rank_check import no_access_rank_check
    from src.discord.colour_check import no_colour_check
    from src.discord.member_list import memberlist

    DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
    discord_bot = DiscordBot()

    @discord_bot.event
    async def on_ready():
        logging.info(f"Logged in as {discord_bot.user} ({discord_bot.user.id})")

        # DB connection
        Database.connect()

        # write an run in db
        add_run(run_type)

        if option == 1:
            await no_access_rank_check()

        elif option == 2:
            await no_colour_check()

        elif option == 3:
            await memberlist()
            

        await quit(discord_bot)

    async with discord_bot:
        await discord_bot.start(DISCORD_BOT_TOKEN)
    

if __name__ == "__main__":
    # process args
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--access', action='store_true')
    parser.add_argument('--colours', action='store_true')
    parser.add_argument('--members', action='store_true')
    args = parser.parse_args()

    option = 0
    if args.access:
        option = 1
        run_type = "access"
    elif args.colours:
        option = 2
        run_type = "colour"
    elif args.members:
        option = 3
        run_type = "members"
    else:
        print("Please use access, colours or members")
        sys.exit(1)

    asyncio.run(main(option, run_type))
