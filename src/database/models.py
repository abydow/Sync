from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.sql import func

from database import Base


class Guild(Base):
    """Guild Config."""

    __tablename__ = "guilds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, unique=True, nullable=False, index=True)
    prefix = Column(String(5), default="!")
    welcome_enabled = Column(Boolean, default=False)
    welcome_message = Column(String(500), default="Welcome {member}!")
    welcome_channel_id = Column(BigInteger, nullable=True)
    modlog_channel_id = Column(BigInteger, nullable=True)
    auto_role_id = Column(BigInteger, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "length(prefix) > 0 AND length(prefix) <= 5", name="valid_prefix"
        ),
    )

    def __repr__(self):
        return f"<Guild {self.guild_id}>"


class User(Base):
    """User Profile"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<User {self.user_id}>"


class ModerationCase(Base):
    """Moderation Action Log"""

    __tablename__ = "moderation_cases"
    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, index=True)
    case_number = Column(Integer, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    moderator_id = Column(BigInteger, nullable=False)
    action = Column(String(50), nullable=False)
    reason = Column(String(500), nullable=False)
    duration = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (CheckConstraint("case_number > 0", name="valid_case_number"),)

    # def __repr__(self):
    #    return f"<ModerationCase {self.guild_id} Case #{self.case_number}>"
