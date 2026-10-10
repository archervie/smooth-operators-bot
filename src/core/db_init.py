import aiosqlite

DB_NAME = "database.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    level INTEGER NOT NULL DEFAULT 1,
    xp_gained INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY
);
"""


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executescript(SCHEMA)
        await db.commit()
    print(f"Database initialized as {DB_NAME}")
