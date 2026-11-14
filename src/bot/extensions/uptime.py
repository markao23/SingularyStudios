import datetime
import discord
from discord import app_commands
from discord.ext import commands

class Uptime(commands.Cog):
    """Slash command that shows how long the bot has been running."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _format_duration(self, delta: datetime.timedelta) -> str:
        """Return a human‑readable string like ``2 days, 3h 04m 05s``."""
        days = delta.days
        seconds = delta.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        parts = []
        if days:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        parts.append(f"{secs}s")
        return ", ".join(parts)

    @app_commands.command(name="uptime", description="Mostra o tempo de atividade do bot.")
    async def uptime(self, interaction: discord.Interaction) -> None:
        """Create an embed with the bot's uptime and send it."""
        now = datetime.datetime.utcnow()
        start = getattr(self.bot, "start_time", now)
        delta = now - start
        embed = discord.Embed(title="🤖 Uptime", color=discord.Color.blue())
        embed.add_field(name="Tempo de atividade", value=self._format_duration(delta), inline=False)
        embed.set_footer(text=self.bot.user.name if self.bot.user else "Bot")
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Uptime(bot))
