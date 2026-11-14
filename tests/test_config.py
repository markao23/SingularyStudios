from pathlib import Path

import pytest

from bot.config import Settings


def test_settings_requires_token(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("DISCORD_TOKEN", raising=False)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("bot.config.load_dotenv", lambda: None)

    with pytest.raises(RuntimeError, match="DISCORD_TOKEN"):
        Settings.from_environment()


def test_settings_reads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.setenv("DISCORD_GUILD_ID", "123")
    monkeypatch.setenv("LOG_LEVEL", "debug")

    settings = Settings.from_environment()

    assert settings.discord_token == "test-token"
    assert settings.discord_guild_id == 123
    assert settings.log_level == "DEBUG"
