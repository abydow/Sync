import time
from typing import Dict, Optional, Set

from models.dto import GuildConfigDTO


class GuildCache:
    """
    Simple in-memory cache for Guild configurations to reduce database hits.
    Stores guild_id existence and config data.
    """

    def __init__(self, ttl: int = 300):
        self._guilds: Set[int] = set()
        self._configs: Dict[int, GuildConfigDTO] = {}
        self._timestamps: Dict[int, float] = {}
        self.ttl = ttl  # Time to live in seconds (default 5 mins)

    def add_guild(self, guild_id: int):
        """Mark a guild as existing in the DB."""
        self._guilds.add(guild_id)

    def has_guild(self, guild_id: int) -> bool:
        """Check if guild exists in cache."""
        return guild_id in self._guilds

    def get_config(self, guild_id: int) -> Optional[GuildConfigDTO]:
        """Get guild config if cached and not expired."""
        if guild_id in self._configs:
            if time.time() - self._timestamps.get(guild_id, 0) < self.ttl:
                return self._configs[guild_id]
            else:
                # Expired
                del self._configs[guild_id]
                del self._timestamps[guild_id]
        return None

    def set_config(self, guild_id: int, config: GuildConfigDTO):
        """Cache guild config."""
        self._configs[guild_id] = config
        self._timestamps[guild_id] = time.time()
        self.add_guild(guild_id)

    def invalidate(self, guild_id: int):
        """Invalidate cache for a guild."""
        if guild_id in self._configs:
            del self._configs[guild_id]
        if guild_id in self._timestamps:
            del self._timestamps[guild_id]
