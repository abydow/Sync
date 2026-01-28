import platform
from datetime import datetime

import discord
from discord.ext import commands
from discord.utils import format_dt

from utils.embeds import EmbedBuilder


def get_uptime(start_time):
    now = datetime.utcnow()
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {minutes}m "


class BasicCommands(commands.Cog):
    # Basic utility commands

    def __init__(self, bot):
        self.bot = bot
        if not hasattr(self.bot, "start_time"):
            self.bot.start_time = datetime.utcnow()

    @commands.command(
        name="ping",
        aliases=["pong", "latency", "lag", "ms", "p"],
        help="Shows the bot's latency",
    )
    async def ping(self, ctx: commands.Context):
        # Bot latency
        latency_ms = round(self.bot.latency * 1000)
        embed = EmbedBuilder.info(ctx, "Latency", f"⌬ **{latency_ms}ms**")
        await ctx.send(embed=embed)

    @commands.command(
        name="botinfo",
        aliases=["bi", "about", "stats", "info", "botstats"],
        help="Shows detailed information about the bot",
    )
    async def info(self, ctx: commands.Context):
        # Bot info
        guilds_count = len(self.bot.guilds)
        users_count = sum(g.member_count for g in self.bot.guilds)
        latency = round(self.bot.latency * 1000)

        discord_ver = discord.__version__

        embed = discord.Embed(
            description=f"**ID:** `{self.bot.user.id}`",
            color=0x2B2D31,
            timestamp=discord.utils.utcnow(),
        )

        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.set_author(
            name=f"{self.bot.user.name} Information",
            icon_url=self.bot.user.display_avatar.url if self.bot.user.avatar else None,
        )
        embed.add_field(
            name="🌎 Servers",
            value=f"```ansi\n\u001b[0;34m{guilds_count:,}\u001b[0m```",
            inline=True,
        )
        embed.add_field(
            name="👥 Users",
            value=f"```ansi\n\u001b[0;34m{users_count:,}\u001b[0m```",
            inline=True,
        )
        embed.add_field(
            name="📡 Latency",
            value=f"```ansi\n\u001b[0;32m{latency} ms\u001b[0m```",
            inline=True,
        )
        embed.add_field(
            name="🖥️ System",
            value=f"`{platform.system()}`",
            inline=True,
        )
        embed.add_field(
            name="📦 Library",
            value=f"`discord.py {discord_ver}`",
            inline=True,
        )
        embed.add_field(
            name="⏱️ Uptime", value=f"`{get_uptime(self.bot.start_time)}`", inline=True
        )

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Invite Me",
                style=discord.ButtonStyle.link,
                url="https://discord.com/oauth2/authorize?client_id=1451878521029791897&permissions=8&integration_type=0&scope=bot",
                emoji="🔗",
            )
        )

        view.add_item(
            discord.ui.Button(
                label="Support",
                style=discord.ButtonStyle.link,
                url="https://discord.gg/Y6dsH9kF",
                emoji="🛡️",
            )
        )

        view.add_item(
            discord.ui.Button(
                label="Github",
                style=discord.ButtonStyle.link,
                url="https://github.com/abydow/Sync",
                emoji="🐙",
            )
        )

        await ctx.send(embed=embed, view=view)

    @commands.command(
        name="userinfo",
        aliases=["ui", "user", "whois", "memberinfo", "profile"],
        help="Shows information about a user",
    )
    async def user_info(self, ctx: commands.Context, member: discord.Member = None):
        # show user info
        member = member or ctx.author
        try:
            user = await self.bot.fetch_user(member.id)
        except discord.NotFound:
            user = None

        embed_color = (
            member.color
            if member.color != discord.Color.default()
            else user.accent_color or discord.Color.teal()
        )
        embed = discord.Embed(color=embed_color)

        user_type = "⚡ Bot" if member.bot else "👨‍👩‍👧‍👦 User"
        embed.set_author(
            name=f"{user_type} • {member.display_name}",
            icon_url=member.display_avatar.url,
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        if user.banner:
            embed.set_image(url=user.banner.url)

        create_ts = int(member.created_at.timestamp())

        description_lines = [
            f"**Handle:** `{member.name}`",
            f"**ID:** `{member.id}`",
            f"**Created:** <t:{create_ts}:F> (<t:{create_ts}:R>)",
        ]

        embed.description = "\n".join(description_lines)

        if member.joined_at:
            joined_ts = int(member.joined_at.timestamp())
            join_str = f"<t:{joined_ts}:F> (<t:{joined_ts}:R>)"
        else:
            join_str = "Unknown"

        key_perms = []
        if member.guild_permissions.administrator:
            key_perms.append("`🛡️ Administrator`")

        elif member.guild_permissions.manage_messages:
            key_perms.append("`🔨 Moderator`")

        perm_str = " | ".join(key_perms) if key_perms else "`Regular Member`"

        embed.add_field(
            name="█ 📍 Server Membership  \n" + "╰───────────────────\n",
            value=f"**Joined:** {join_str}\n**Top Role:** {member.top_role.mention}\n**Access:** {perm_str}",
            inline=False,
        )

        roles = [role for role in member.roles if role.name != "@everyone"]
        roles.reverse()

        if roles:
            role_mentions = [r.mention for r in roles]
            if len(roles) > 8:
                roles_str = (
                    " ".join(role_mentions[:8]) + f" ... and **{len(roles) - 8}** more"
                )
            else:
                roles_str = " ".join(role_mentions)

        else:
            roles_str = "No roles assigned."

        embed.add_field(
            name=f"█ 🎭 Roles [{len(roles)}] \n" + "╰──────────\n",
            value=roles_str,
            inline=False,
        )

        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )
        embed.timestamp = ctx.message.created_at

        await ctx.send(embed=embed)
        """
        embed1 = discord.Embed(
            title="👤 User Information", color=discord.Color.blurple()
        )
        embed1.add_field(name="Name", value=member.name, inline=False)
        embed1.add_field(name="Display Name", value=member.display_name, inline=False)
        embed1.add_field(name="ID", value=member.id, inline=False)
        embed1.add_field(
            name="Created At",
            value=member.created_at.strftime("%Y-%m-%d %H:%M"),
            inline=False,
        )
        embed1.add_field(name="Bot", value="Yes" if member.bot else "No", inline=False)
        embed1.set_image(url=member.display_avatar.url)

        if ctx.guild and isinstance(member, discord.Member):
            embed2 = discord.Embed(
                title="🫱🏼‍🫲🏾 Guild Member info", color=discord.Color.magenta()
            )
            embed2.add_field(
                name="Joined",
                value=member.joined_at.strftime("%Y-%m-%d %H:%M"),
                inline=False,
            )
            embed2.add_field(name="Nickname", value=member.nick or "None", inline=False)
            embed2.add_field(
                name="Top Role", value=member.top_role.mention, inline=False
            )

            # Show roles (highest to lowest, excluding @everyone)
            roles = member.roles[1:][::-1]
            role_mentions = [r.mention for r in roles[:10]]
            embed2.add_field(
                name="Roles",
                value=f"{(len(member.roles) - 1)}: {', '.join(role_mentions) or 'None'}",
            )

            if len(roles) > 10:
                embed2.add_field(name=f" ... and {len(roles) - 10} more")

        await ctx.send(embeds=[embed1, embed2] if "embed2" in locals() else [embed1])
        """

    @user_info.error
    async def user_info_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MemberNotFound):
            embed = EmbedBuilder.error(
                ctx, "User Not Found", f"Could not find member '{error.argument}'."
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="serverinfo",
        aliases=["si", "server", "guild", "guildinfo", "aboutserver"],
        help="Shows information about the server",
    )
    async def server_info(self, ctx: commands.Context):
        # Show server information
        guild = ctx.guild

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        threads = len(guild.threads)
        categories = len(guild.categories)

        role_count = len(guild.roles)
        emoji_count = len(guild.emojis)
        sticker_count = len(guild.stickers)
        boost_count = guild.premium_subscription_count or 0
        boost_tier = guild.premium_tier

        icon_url = guild.icon.url if guild.icon else None
        banner_url = guild.banner.url if guild.banner else None

        desc = f"_{guild.description}_" if guild.description else ""

        embed = discord.Embed(
            description=desc,
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow(),
        )

        embed.set_author(name=f"{guild.name}", icon_url=icon_url)
        if icon_url:
            embed.set_thumbnail(url=icon_url)
        if banner_url:
            embed.set_image(url=banner_url)

        embed.add_field(
            name="👑 Owner",
            value=f"{guild.owner.mention if guild.owner else 'Unknown'}",
            inline=True,
        )
        embed.add_field(
            name="📅 Created",
            value=format_dt(guild.created_at, "R"),
            inline=True,
        )
        embed.add_field(
            name="🆔 Server ID",
            value=f"`{guild.id}`",
            inline=True,
        )

        stats_value = (
            f"█ 👥 **Members:** {guild.member_count}\n"
            f"█ 🚀 **Boosts:** Tier {boost_tier} ({boost_count} boosts)\n"
            f"█ 🔐 **Verification:** {str(guild.verification_level).title()}"
        )
        embed.add_field(
            name="\n█═══════╗\n" + "█  Statistics  ║\n" + "█═══════╝\n",
            value=stats_value,
            inline=False,
        )

        channels_value = (
            f"█ 💬 **Text:** {text_channels} | 🔊 **Voice:** {voice_channels}\n"
            f"█ 🧵 **Threads:** {threads} | 📂 **Categories:** {categories}"
        )
        embed.add_field(
            name="\n█═══════╗\n" + "█  Channels  ║\n" + "█═══════╝\n",
            value=channels_value,
            inline=False,
        )

        inventory_value = (
            f"█ 🎭 **Roles:** {role_count}\n"
            f"█ 😀 **Emojis:** {emoji_count} | 🏷️ **Stickers:** {sticker_count}"
        )
        embed.add_field(
            name="\n█═══════╗\n" + "█  Inventory  ║\n" + "█═══════╝\n",
            value=inventory_value,
            inline=False,
        )

        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        await ctx.send(embed=embed)
        """
        embed.add_field(name="Name", value=guild.name, inline=False)
        embed.add_field(name="ID", value=guild.id, inline=False)
        embed.add_field(
            name="Owner",
            value=guild.owner.mention if guild.owner else "Unknown",
            inline=False,
        )
        embed.add_field(
            name="Created",
            value=guild.created_at.strftime("%Y-%m-%d %H:%M"),
            inline=False,
        )
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(
            name="Channels",
            value=f"{text_channels} text channels, {voice_channels} voice channels",
            inline=False,
        )
        embed.add_field(name="Roles", value=roles, inline=False)
        embed.add_field(
            name="Verification Level", value=guild.verification_level, inline=False
        )
        await ctx.send(embed=embed)
        """


# Setup


async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
