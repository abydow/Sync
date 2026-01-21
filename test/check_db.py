#!/usr/bin/env python3
"""
Script to test DatabaseService.get_or_create_guild.

Example:
    python src/scripts/check_db.py 1452632091488419923
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from argparse import ArgumentParser

from dotenv import load_dotenv

# Ensure local 'src' package dir is importable regardless of cwd
HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(HERE, ".."))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

load_dotenv()

# Import after we've adjusted sys.path
from sqlalchemy import select  # noqa: E402

from database import AsyncSessionLocal, init_db  # noqa: E402
from database.models import Guild  # noqa: E402
from database.service import DatabaseService  # noqa: E402


async def run_check(guild_id: int) -> None:
    logging.info("Initializing database (creating tables if needed)...")
    await init_db()

    async with AsyncSessionLocal() as session:
        # Check if guild already exists
        result = await session.execute(select(Guild).where(Guild.guild_id == guild_id))
        existing = result.scalar_one_or_none()
        if existing:
            logging.info("Guild already exists in database.")
        else:
            logging.info(
                "Guild does not exist yet. Calling get_or_create_guild to create it."
            )

        db = DatabaseService(session)
        guild = await db.get_or_create_guild(guild_id)

        print("\nGuild record:")
        print(f"  id:                {guild.id}")
        print(f"  guild_id:          {guild.guild_id}")
        print(f"  prefix:            {guild.prefix}")
        print(f"  welcome_enabled:   {guild.welcome_enabled}")
        print(f"  welcome_message:   {guild.welcome_message}")
        print(f"  welcome_channel_id:{guild.welcome_channel_id}")
        print(f"  modlog_channel_id: {guild.modlog_channel_id}")
        print(f"  auto_role_id:      {guild.auto_role_id}")
        print(f"  created_at:        {guild.created_at}")
        print(f"  updated_at:        {guild.updated_at}")
        print()


def parse_args() -> int:
    parser = ArgumentParser(description="Quick database check for get_or_create_guild")
    parser.add_argument(
        "guild_id",
        nargs="?",
        type=int,
        default=1452632091488419923,
        help="Guild ID to check/create (default: 1452632091488419923)",
    )
    ns = parser.parse_args()
    return ns.guild_id


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    guild_id = parse_args()
    try:
        asyncio.run(run_check(guild_id))
        return 0
    except (
        Exception
    ) as exc:  # pragma: no cover - small script, surface exception to user
        logging.exception("Error while checking/creating guild: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
