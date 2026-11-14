import datetime

import asyncio


import logging
import os
from logging.handlers import RotatingFileHandler
import sys
import watchtower
from discord.ext import commands

# Logging configuration
def setup_logging():
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "bot.log")
    handler = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(handler)
    # CloudWatch handler (requires AWS env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION)
    try:
        cw_handler = watchtower.CloudWatchLogHandler(log_group="singulary-bot-logs", stream_name="bot-stream")
        cw_handler.setFormatter(formatter)
        root.addHandler(cw_handler)
    except Exception as e:
        root.error("Failed to configure CloudWatch logging: %s", e)

setup_logging()

from bot.config import Settings

EXTENSIONS = ("bot.extensions.general", "bot.extensions.uptime",)


class DiscordBot(commands.Bot):
    def __init__(self, settings: Settings) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
    
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
            help_command=None,

        )
        self.settings = settings
        self.start_time = datetime.datetime.utcnow()

    async def setup_hook(self) -> None:
        for extension in EXTENSIONS:
            await self.load_extension(extension)

        if self.settings.discord_guild_id is not None:
            guild = discord.Object(id=self.settings.discord_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logging.getLogger(__name__).info(
                "Comandos sincronizados na guild %s", self.settings.discord_guild_id
            )
        else:
            await self.tree.sync()
            logging.getLogger(__name__).info("Comandos globais sincronizados")

    async def on_ready(self) -> None:
        if self.user is not None:
            logging.getLogger(__name__).info(
                "Bot conectado como %s (ID: %s)", self.user, self.user.id
            )


def run() -> None:
    settings = Settings.from_environment()
    # logging.basicConfig(
    #     level=getattr(logging, settings.log_level, logging.INFO),
    #     format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    # )
    bot = DiscordBot(settings)
    asyncio.run(bot.start(settings.discord_token))


if __name__ == "__main__":
    run()

