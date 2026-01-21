import discord


class EmbedBuilder:
    """Helper class for creating consistent embeds"""

    @staticmethod
    def success(title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create Success Embed"""
        embed = discord.Embed(
            title=f"✔ {title}",
            description=description,
            color=discord.Color.green(),
            **kwargs,
        )

        return embed

    @staticmethod
    def error(title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create error embed"""
        embed = discord.Embed(
            title=f"✕ {title}",
            description=description,
            color=discord.Color.red(),
            **kwargs,
        )
        return embed

    @staticmethod
    def info(title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create info embed"""
        embed = discord.Embed(
            title=f"ℹ️ {title}",
            description=description,
            color=discord.Color.bule(),
            **kwargs,
        )

        return embed

    @staticmethod
    def warning(title: str, description: str = "", **kwargs) -> discord.Embed:
        """Create warning embed"""
        embed = discord.Embed(
            title=f"⚠️ {title}",
            description=description,
            color=discord.Color.gold(),
            **kwargs,
        )

        return embed
