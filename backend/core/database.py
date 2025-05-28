# backend/core/database.py
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


class Database:
    def __init__(self):
        self._pool = None

    async def connect(self):
        if not self._pool:
            self._pool = await asyncpg.create_pool(
                dsn=DATABASE_URL, min_size=1, max_size=10
            )
        return self._pool

    async def disconnect(self):
        if self._pool:
            await self._pool.close()
            self._pool = None


database = Database()
