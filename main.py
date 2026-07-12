import asyncio
from dotenv import load_dotenv
import logging
import os

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

async def main():
    logging.info("Hello!")
    DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]

    discord_bot = DiscordBot()

    @discord_bot.event
    async def on_ready():
        logging.info(f"Logged in as {discord_bot.user} ({discord_bot.user.id})")

        # Add your other functions here (scan servers, check DBs, etc.)

        # Uncomment to have bot quit when finished running any code here.
        #await quit(discord_bot)

    async with discord_bot:
        await discord_bot.start(DISCORD_BOT_TOKEN)
    

if __name__ == "__main__":
    asyncio.run(main())
