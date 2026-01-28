import unittest
from unittest.mock import MagicMock

import discord

from utils.embeds import EmbedBuilder


class TestEmbedBuilder(unittest.TestCase):
    def setUp(self):
        # Mock Context
        self.ctx = MagicMock()
        self.ctx.author.name = "TestUser"
        self.ctx.author.avatar.url = "http://example.com/avatar.png"
        self.ctx.me.display_avatar.url = "http://example.com/bot_avatar.png"
        self.ctx.me.avatar = True  # To ensure avatar check passes

        # Mock Bot (for client/bot access in _build_embed logic if needed)
        # In _build_embed:
        # user = ctx.user if isinstance(ctx, discord.Interaction) else ctx.author
        # bot_user = ctx.client.user if isinstance(ctx, discord.Interaction) else ctx.me
        # bot = ctx.client if isinstance(ctx, discord.Interaction) else ctx.bot

        # We need to simulate ctx.bot for non-Interaction context
        self.ctx.bot.user.avatar.url = "http://example.com/bot_avatar.png"
        self.ctx.bot.user.avatar = True

    def test_success_embed(self):
        embed = EmbedBuilder.success(self.ctx, "Success Title", "Success Description")

        self.assertIsInstance(embed, discord.Embed)
        self.assertEqual(embed.title, "✅ Success Title")
        self.assertEqual(embed.description, "Success Description")
        self.assertEqual(embed.color.value, 0x57F287)  # Green
        self.assertEqual(embed.footer.text, "Requested by TestUser")

    def test_error_embed(self):
        embed = EmbedBuilder.error(self.ctx, "Error Title", "Error Description")

        self.assertIsInstance(embed, discord.Embed)
        self.assertEqual(embed.title, "❌ Error Title")
        self.assertEqual(embed.description, "Error Description")
        self.assertEqual(embed.color.value, 0xED4245)  # Red

    def test_info_embed(self):
        embed = EmbedBuilder.info(self.ctx, "Info Title", "Info Description")

        self.assertIsInstance(embed, discord.Embed)
        self.assertEqual(embed.title, "🔍 Info Title")
        self.assertEqual(embed.description, "Info Description")
        self.assertEqual(embed.color.value, 0x5865F2)  # Blurple

    def test_warning_embed(self):
        embed = EmbedBuilder.warning(self.ctx, "Warning Title", "Warning Description")

        self.assertIsInstance(embed, discord.Embed)
        self.assertEqual(embed.title, "⚠️ Warning Title")
        self.assertEqual(embed.description, "Warning Description")
        self.assertEqual(embed.color.value, 0xFEE75C)  # Yellow


if __name__ == "__main__":
    unittest.main()
