from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    LOG_DIR: Path = BASE_DIR / "logs"

    # Bot Configuration
    DISCORD_TOKEN: str = Field(..., description="Discord Bot Token")
    COMMAND_PREFIX: str = Field(default="!", max_length=5)
    OWNER_IDS: List[int] = Field(default_factory=list)

    # Database
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./bot.db")

    # Links
    SUPPORT_SERVER_URL: str = "https://discord.gg/Y6dsH9kF"
    GITHUB_REPO_URL: str = "https://github.com/abydow/Sync"

    # Feature Flags / Defaults
    DEFAULT_WELCOME_MESSAGE: str = "Welcome {member} to {server}!"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)

    @property
    def PREFIX(self) -> str:
        return self.COMMAND_PREFIX


settings = Settings()
