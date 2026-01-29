from typing import Optional, Union

import discord
from discord.ext import commands


class EmbedBuilder:
    """Helper class for creating consistent embeds"""

    @staticmethod
    def _build_embed(
        ctx: Optional[Union[discord.Interaction, commands.Context]],
        title: str,
        description: str,
        color: int,
        emoji: str,
        **kwargs,
    ) -> discord.Embed:
        embed = discord.Embed(
            title=f"{emoji} {title}",
            description=description,
            color=color,
            timestamp=discord.utils.utcnow(),
            **kwargs,
        )

        if ctx:
            user = ctx.user if isinstance(ctx, discord.Interaction) else ctx.author
            # Check if ctx.client exists (Interaction) or ctx.me (Context)
            if isinstance(ctx, discord.Interaction):
                bot_user = ctx.client.user
            else:
                bot_user = ctx.me

            if user:
                icon_url = user.avatar.url if user.avatar else None
                embed.set_footer(
                    text=f"Requested by {user.name}",
                    icon_url=icon_url,
                )

            if bot_user:
                # Check for display_avatar (safer than avatar which might be None)
                avatar_url = bot_user.display_avatar.url
                embed.set_thumbnail(url=avatar_url)

        return embed

    @staticmethod
    def success(
        ctx: Optional[Union[discord.Interaction, commands.Context]],
        title: str,
        description: str = "",
        **kwargs,
    ) -> discord.Embed:
        """Create Success Embed"""
        return EmbedBuilder._build_embed(
            ctx, title, description, color=0x57F287, emoji="✅", **kwargs
        )

    @staticmethod
    def error(
        ctx: Optional[Union[discord.Interaction, commands.Context]],
        title: str,
        description: str = "",
        **kwargs,
    ) -> discord.Embed:
        """Create Error Embed"""
        return EmbedBuilder._build_embed(
            ctx, title, description, color=0xED4245, emoji="❌", **kwargs
        )

    @staticmethod
    def info(
        ctx: Optional[Union[discord.Interaction, commands.Context]],
        title: str,
        description: str = "",
        **kwargs,
    ) -> discord.Embed:
        """Create Info Embed"""
        return EmbedBuilder._build_embed(
            ctx, title, description, color=0x99AAB5, emoji="🔍", **kwargs
        )

    @staticmethod
    def warning(
        ctx: Optional[Union[discord.Interaction, commands.Context]],
        title: str,
        description: str = "",
        **kwargs,
    ) -> discord.Embed:
        """Create Warning Embed"""
        return EmbedBuilder._build_embed(
            ctx, title, description, color=0xFEE75C, emoji="⚠️", **kwargs
        )
