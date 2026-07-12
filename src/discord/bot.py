import discord
from discord.ext import commands
import logging


class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds          = True # Events related to servers, such as on_guild_join or on_guild_update
        intents.message_content = True # Access to the content of messages (needed to read messages)
        intents.members         = True # Events and data related to server members (e.g., member join/leave, fetching member list)
        intents.presences       = True # Updates about user presence (e.g., online, offline, idle, do not disturb)
        intents.messages        = True # Message-related events like on_message, on_message_edit, on_message_delete

        super().__init__(
            command_prefix="/",
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self):
        logging.info("Registering commands...")

        await self.load_extension("src.discord.commands.ping")
        await self.load_extension("src.discord.commands.quit")

        logging.info("Syncing command tree with Discord...")
        try:
            await self.tree.sync()
            logging.info(f"Slash commands (global) synced")
        except Exception as e:
            logging.error(f"{e}")
