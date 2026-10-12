import logging

import aiosqlite

logger = logging.getLogger(__name__)
DB_NAME = "database.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    level INTEGER NOT NULL DEFAULT 1,
    xp_gained INTEGER NOT NULL DEFAULT 0,
    title TEXT NOT NULL DEFAULT 'Subscriber'
);

CREATE INDEX IF NOT EXISTS idx_users_xp ON users (xp_gained DESC);
"""


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executescript(SCHEMA)
        await db.execute("PRAGMA journal_mode=WAL;")
        await db.commit()
    logger.info(f"Database initialized as {DB_NAME}")
