from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Guild, User


class DatabaseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_guild(self, guild_id: int) -> Guild:
        """Get Guild Config or Create"""
        result = await self.session.execute(
            select(Guild).where(Guild.guild_id == guild_id)
        )
        guild = result.scalar_one_or_none()

        if not guild:
            guild = Guild(guild_id=guild_id)
            self.session.add(guild)
            try:
                await self.session.commit()
            except IntegrityError:
                await self.session.rollback()
                result = await self.session.execute(
                    select(Guild).where(Guild.guild_id == guild_id)
                )
                guild = result.scalar_one()

        return guild

    async def get_guild_config(self, guild_id: int) -> dict:
        """Get Guild Config."""
        guild = await self.get_or_create_guild(guild_id)
        return {
            "prefix": guild.prefix,
            "welcome_enabled": guild.welcome_enabled,
            "welcome_message": guild.welcome_message,
            "welcome_channel_id": guild.welcome_channel_id,
            "modlog_channel_id": guild.modlog_channel_id,
            "auto_role_id": guild.auto_role_id,
        }

    async def update_guild_prefix(self, guild_id: int, prefix: str):
        """update guild command prefix"""
        await self.session.execute(
            update(Guild).where(Guild.guild_id == guild_id).values(prefix=prefix)
        )
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def update_welcome_settings(
        self, guild_id: int, enabled: bool, channel_id: int, message: str
    ):
        """Update welcome message settings"""
        await self.session.execute(
            update(Guild)
            .where(Guild.guild_id == guild_id)
            .values(
                welcome_enabled=enabled,
                welcome_channel_id=channel_id,
                welcome_message=message,
            )
        )
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def get_or_create_user(self, user_id: int, username: str) -> User:
        """Get User or Create"""
        result = await self.session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            user = User(user_id=user_id, username=username)
            self.session.add(user)
            try:
                await self.session.commit()
            except IntegrityError:
                await self.session.rollback()
                result = await self.session.execute(
                    select(User).where(User.user_id == user_id)
                )
                user = result.scalar_one()

        return user
