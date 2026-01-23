import discord


class EmbedBuilder:
    """Helper class for creating consistent embeds"""

    @staticmethod
    def success(title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Success Embed"""
        embed = discord.Embed(
            title=f"✔ {title}",
            description=description,
            color=discord.Color.from_rgb(0, 255, 0),
            **kwargs,
        )

        return embed

    @staticmethod
    def error(title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Error Embed"""
        embed = discord.Embed(
            title=f"✕ {title}",
            description=description,
            color=discord.Color.from_rgb(255, 0, 0),
            **kwargs,
        )
        return embed

    @staticmethod
    def info(title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Info Embed"""
        embed = discord.Embed(
            title=f"ℹ️ {title}",
            description=description,
            color=discord.Color.from_rgb(0, 0, 255),
            **kwargs,
        )

        return embed

    @staticmethod
    def warning(title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Warning Embed"""
        embed = discord.Embed(
            title=f"⚠️ {title}",
            description=description,
            color=discord.Color.from_rgb(255, 255, 0),
            **kwargs,
        )

        return embed
