from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Optional, Tuple

import discord

from config.logger import setup_logging


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
