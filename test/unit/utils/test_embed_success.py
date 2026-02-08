import unittest
from unittest.mock import MagicMock
import discord
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from utils.embeds import EmbedBuilder

class TestEmbedSuccess(unittest.TestCase):
    def setUp(self):
        self.ctx = MagicMock()
        self.ctx.author.name = "TestUser"
        self.ctx.author.avatar.url = "http://example.com/avatar.png"
        self.ctx.me.display_avatar.url = "http://example.com/bot_avatar.png"
        self.ctx.me.avatar = True
        self.ctx.bot.user.avatar.url = "http://example.com/bot_avatar.png"
        self.ctx.bot.user.avatar = True

    def test_success_embed(self):
        embed = EmbedBuilder.success(self.ctx, "Success Title", "Success Description")
        self.assertIsInstance(embed, discord.Embed)
        self.assertEqual(embed.title, "✅ Success Title")
        self.assertEqual(embed.description, "Success Description")
        self.assertEqual(embed.color.value, 0x57F287)
        self.assertEqual(embed.footer.text, "Requested by TestUser")

if __name__ == "__main__":
    unittest.main()
