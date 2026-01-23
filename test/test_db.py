import asyncio
import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


@pytest.mark.asyncio
async def test_connection():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL not found in .env file!")

    try:
        print("🔗 Attempting to connect to database...")
        engine = create_async_engine(DATABASE_URL, echo=False, future=True)
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
            print("✅ Connection successful!")
        await engine.dispose()
    except Exception as e:
        pytest.fail(f"Connection failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_connection())
