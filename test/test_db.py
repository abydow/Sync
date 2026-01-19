import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


async def test_connection():
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in .env file!")
        return

    try:
        print("🔗 Attempting to connect to database...")
        engine = create_async_engine(DATABASE_URL, echo=False, future=True)
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
            print("✅ Connection successful!")
        await engine.dispose()
    except Exception as e:
        print(f"❌ Connection failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_connection())
