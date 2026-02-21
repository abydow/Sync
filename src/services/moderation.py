import logging
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ModerationCase

logger = logging.getLogger(__name__)


class ModerationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_case(
        self,
        guild_id: int,
        user_id: int,
        moderator_id: int,
        action: str,
        reason: str,
        duration: Optional[int] = None,
    ) -> ModerationCase:
        """
        Log a moderation action with race condition handling (Optimistic Concurrency).
        """
        retries = 3
        while retries > 0:
            try:
                # Get max case number
                result = await self.session.execute(
                    select(func.max(ModerationCase.case_number)).where(
                        ModerationCase.guild_id == guild_id
                    )
                )
                max_case = result.scalar() or 0
                next_case = max_case + 1

                case = ModerationCase(
                    guild_id=guild_id,
                    case_number=next_case,
                    user_id=user_id,
                    moderator_id=moderator_id,
                    action=action,
                    reason=reason,
                    duration=duration,
                )
                self.session.add(case)
                await self.session.commit()
                return case

            except IntegrityError:
                # Likely a duplicate key error on (guild_id, case_number)
                await self.session.rollback()
                logger.warning(
                    f"Race condition detected for guild {guild_id} case #{next_case}, retrying..."
                )
                retries -= 1

        raise Exception("Failed to log moderation case after multiple retries")
