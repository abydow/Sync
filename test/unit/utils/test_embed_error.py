import unittest
from unittest.mock import MagicMock
import discord
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from utils.embeds import EmbedBuilder

class TestEmbedError(unittest.TestCase):
    def setUp(self):
        self.ctx = MagicMock()
        self.ctx.author.name = "TestUser"
        self.ctx.author.avatar.url = "http://example.com/avatar.png"
        self.ctx.me.display_avatar.url = "http://example.com/bot_avatar.png"
        self.ctx.me.avatar = True
        self.ctx.bot.user.avatar.url = "http://example.com/bot_avatar.png"
        self.ctx.bot.user.avatar = True

    def test_error_embed(self):
        embed = EmbedBuilder.error(self.ctx, "Error Title", "Error Description")
        self.assertIsInstance(embed, discord.Embed)
        self.assertEqual(embed.title, "❌ Error Title")
        self.assertEqual(embed.description, "Error Description")
        self.assertEqual(embed.color.value, 0xED4245)

if __name__ == "__main__":
    unittest.main()
