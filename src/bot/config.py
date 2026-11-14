from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class Settings:
    discord_token: str
    discord_guild_id: int | None
    log_level: str

    @classmethod
    def from_environment(cls) -> "Settings":
        load_dotenv()

        token = os.getenv("DISCORD_TOKEN", "").strip()
        if not token:
            raise RuntimeError(
                "DISCORD_TOKEN não foi definido. Copie .env.example para .env e informe o token."
            )

        raw_guild_id = os.getenv("DISCORD_GUILD_ID", "").strip()
        guild_id = int(raw_guild_id) if raw_guild_id else None
        return cls(
            discord_token=token,
            discord_guild_id=guild_id,
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )

