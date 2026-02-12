import logging
from collections import defaultdict, deque
from datetime import datetime
from typing import Optional, Tuple

import discord

logger = logging.getLogger(__name__)


class AntiSpamService:
    # Track User message history and detects spam patterns

    def __init__(self):
        # Store last ten
        self._user_history = defaultdict(lambda: deque(maxlen=10))

        # Threshholds
        self.RATE_LIMIT_THRESHOLD = 5  # Max messages
        self.RATE_LIMIT_WINDOW = 5.0  # Timelimit = 5s
        self.DUPLICATE_THRESHOLD = 4  # Max Identical messages
        self.DUPLICATE_WINDOW = 10.0  # Timelimit = 10s

    def check_spam(self, message: discord.Message) -> Tuple[bool, Optional[str]]:
        # Checking

        user_id = message.author.id
        now = datetime.now()
        content = message.content

        # Current message history

        history = self._user_history[user_id]
        history.append((now, content))

        """Rate limit check"""

        def last_count():

            for t, _ in history:
                if (now - t).total_seconds() < self.RATE_LIMIT_WINDOW:
                    yield 1

        recent_count = sum(last_count())

        if recent_count > self.RATE_LIMIT_THRESHOLD:
            return True, " ▰▰▰ RATE LIMIT HIT  ▰▰▰ \n  (You're going too fast!)"

        """Duplicate message check"""

        def dupli_count():

            for t, c in history:
                if c == content and (now - t).total_seconds() < self.DUPLICATE_WINDOW:
                    yield 1

        duplicate_count = sum(dupli_count())

        if duplicate_count >= self.DUPLICATE_THRESHOLD:
            return True, " ▰▰▰ DUPLICATE MESSAGE SPAM ▰▰▰ "

        return False, None

    def clear_user_history(self, user_id: int):
        # Reset
        if user_id in self._user_history:
            del self._user_history[user_id]
