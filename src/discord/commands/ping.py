import discord
from discord import app_commands
from discord.ext import commands

CMD_NAME = "ping"
CMD_DESC = "this is a description"


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name=CMD_NAME, description=CMD_DESC)
    async def ping_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(":stopwatch: | pong!")

async def setup(bot):
    await bot.add_cog(Ping(bot))
