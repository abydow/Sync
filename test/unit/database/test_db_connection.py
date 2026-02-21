import asyncio
import os
import sys
import pytest
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

@pytest.mark.asyncio
async def test_connection():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL not found in .env file!")

    try:
        engine = create_async_engine(DATABASE_URL, echo=False, future=True)
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        await engine.dispose()
    except Exception as e:
        pytest.fail(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
