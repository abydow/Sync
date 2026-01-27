from typing import Union

import discord
from discord.ext import commands


class EmbedBuilder:
    """Helper class for creating consistent embeds"""

    @staticmethod
    def _build_embed(
        ctx: Union[discord.Interaction, commands.Context],
        title: str,
        description: str,
        color: int,
        emoji: str,
        **kwargs,
    ) -> discord.Embed:
        user = ctx.user if isinstance(ctx, discord.Interaction) else ctx.author
        bot_user = ctx.client.user if isinstance(ctx, discord.Interaction) else ctx.me

        embed = discord.Embed(
            title=f"{emoji} {title}",
            description=description,
            color=color,
            timestamp=discord.utils.utcnow(),
            **kwargs,
        )

        embed.set_footer(
            text=f"Requested by {user.name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )
        embed.set_thumbnail(
            url=bot_user.display_avatar.url if bot_user.avatar else None
        )
        return embed

    @staticmethod
    def success(ctx, title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Success Embed"""
        return EmbedBuilder._build_embed(
            ctx, title, description, color=0x57F287, emoji="✅", **kwargs
        )

    @staticmethod
    def error(ctx, title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Error Embed"""
        return EmbedBuilder._build_embed(
            ctx, title, description, color=0xED4245, emoji="❌", **kwargs
        )

    @staticmethod
    def info(ctx, title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Info Embed"""
        return EmbedBuilder._build_embed(
            ctx, title, description, color=0x99AAB5, emoji="🔍", **kwargs
        )

    @staticmethod
    def warning(ctx, title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Warning Embed"""
        return EmbedBuilder._build_embed(
            ctx, title, description, color=0xFEE75C, emoji="⚠️", **kwargs
        )
