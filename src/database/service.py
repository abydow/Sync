from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Guild, User
from models.dto import GuildConfigDTO


class DatabaseService:
    def __init__(self, session: AsyncSession, cache=None):
        self.session = session
        self.cache = cache

    async def _safe_commit(self):
        """Helper to safely commit or rollback changes."""
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def get_or_create_guild(self, guild_id: int) -> Guild:
        """Get Guild or Create if not exists (UPSERT)."""
        stmt = insert(Guild).values(guild_id=guild_id).on_conflict_do_nothing(index_elements=['guild_id'])
        await self.session.execute(stmt)
        await self._safe_commit()

        result = await self.session.execute(select(Guild).where(Guild.guild_id == guild_id))
        return result.scalar_one()

    async def get_guild_config(self, guild_id: int) -> GuildConfigDTO:
        """Get Guild Config with Caching."""
        # 1. Check Cache
        if self.cache:
            cached_config = self.cache.get_config(guild_id)
            if cached_config:
                return cached_config

        # 2. DB Fetch
        guild = await self.get_or_create_guild(guild_id)
        
        dto = GuildConfigDTO(
            prefix=guild.prefix,
            welcome_enabled=guild.welcome_enabled,
            welcome_message=guild.welcome_message,
            welcome_channel_id=guild.welcome_channel_id,
            modlog_channel_id=guild.modlog_channel_id,
            auto_role_id=guild.auto_role_id,
        )

        # 3. Update Cache
        if self.cache:
            self.cache.set_config(guild_id, dto)

        return dto

    async def update_guild_prefix(self, guild_id: int, prefix: str):
        """Update guild command prefix."""
        await self.session.execute(
            update(Guild).where(Guild.guild_id == guild_id).values(prefix=prefix)
        )
        await self._safe_commit()
        
        if self.cache:
            self.cache.invalidate(guild_id)

    async def update_welcome_settings(
        self, guild_id: int, enabled: bool, channel_id: int, message: str
    ):
        """Update welcome message settings."""
        await self.session.execute(
            update(Guild)
            .where(Guild.guild_id == guild_id)
            .values(
                welcome_enabled=enabled,
                welcome_channel_id=channel_id,
                welcome_message=message,
            )
        )
        await self._safe_commit()
        
        if self.cache:
            self.cache.invalidate(guild_id)

    async def get_or_create_user(self, user_id: int, username: str) -> User:
        """Get User or Create if not exists (UPSERT)."""
        stmt = insert(User).values(user_id=user_id, username=username).on_conflict_do_nothing(index_elements=['user_id'])
        await self.session.execute(stmt)
        await self._safe_commit()

        result = await self.session.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one()
