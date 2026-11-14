import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Verifica a latência do bot.")
    async def ping(self, interaction: discord.Interaction) -> None:
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! Latência: {latency_ms} ms.")

    @commands.command(name="ping")
    async def prefix_ping(self, context: commands.Context[commands.Bot]) -> None:
        latency_ms = round(self.bot.latency * 1000)
        await context.send(f"Pong! Latência: {latency_ms} ms.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))

