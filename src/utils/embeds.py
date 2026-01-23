import discord


class EmbedBuilder:
    """Helper class for creating consistent embeds"""

    @staticmethod
    def success(title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Success Embed"""
        embed = discord.Embed(
            title=f"✔ {title}",
            description=description,
            color=discord.Color.from_rgb(205, 67, 158),
            **kwargs,
        )

        return embed

    @staticmethod
    def error(title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Error Embed"""
        embed = discord.Embed(
            title=f"✕ {title}",
            description=description,
            color=discord.Color.from_rgb(162, 50, 111),
            **kwargs,
        )
        return embed

    @staticmethod
    def info(title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Info Embed"""
        embed = discord.Embed(
            title=f"ℹ️ {title}",
            description=description,
            color=discord.Color.from_rgb(252, 214, 91),
            **kwargs,
        )

        return embed

    @staticmethod
    def warning(title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Warning Embed"""
        embed = discord.Embed(
            title=f"⚠️ {title}",
            description=description,
            color=discord.Color.from_rgb(23, 22, 44),
            **kwargs,
        )

        return embed
