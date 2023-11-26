import os

import asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

from models import Base
from src.tasks import compare_result_fc_get_post


async def main() -> None:
    load_dotenv()
    engine = create_async_engine(os.getenv("ASYNC_DB_URL"), echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
