import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Base Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    LOG_DIR = BASE_DIR / "logs"

    # Bot Configuration
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    PREFIX = os.getenv("COMMAND_PREFIX", "!")
    OWNER_IDS = [int(id) for id in os.getenv("OWNER_IDS", "").split(",") if id.strip()]

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bot.db")

    # Links
    SUPPORT_SERVER_URL = os.getenv("SUPPORT_SERVER_URL", "https://discord.gg/Y6dsH9kF")
    GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL", "https://github.com/abydow/Sync")

    # Feature Flags / Defaults
    DEFAULT_WELCOME_MESSAGE = "Welcome {member} to {server}!"

    @classmethod
    def validate(cls):
        """Validate critical configuration"""
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN not found in environment variables.")


# Create logs directory if it doesn't exist
Settings.LOG_DIR.mkdir(parents=True, exist_ok=True)
