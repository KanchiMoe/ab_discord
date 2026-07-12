import discord
from discord import app_commands
from discord.ext import commands
import logging

async def quit(bot: commands.Bot):
    logging.info("Bot is quitting...")
    
    await bot.close()

def is_owner():
    async def predicate(interaction: discord.Interaction):
        return await interaction.client.is_owner(interaction.user)
    return app_commands.check(predicate)

CMD_NAME = "quit"
CMD_DESC = "The bot quits"


class Quit(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name=CMD_NAME, description=CMD_DESC)
    @is_owner()
    async def quit_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="Bot has quit.", ephemeral=True)
        await quit(self.bot)

async def setup(bot):
    await bot.add_cog(Quit(bot))
