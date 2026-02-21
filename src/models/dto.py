from dataclasses import dataclass
from typing import Optional


@dataclass
class GuildConfigDTO:
    """Data Transfer Object for Guild Configuration"""

    prefix: str
    welcome_enabled: bool
    welcome_message: str
    welcome_channel_id: Optional[int]
    modlog_channel_id: Optional[int]
    auto_role_id: Optional[int]
