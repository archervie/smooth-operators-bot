import logging

import aiosqlite
import discord
from discord.ext import commands

from config import config_loader

logger = logging.getLogger(__name__)


class BaseGroupCog(commands.GroupCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.config = config_loader()
        self.db_name = self.config["database"]["name"]

    @property
    def GUILD(self) -> discord.Guild | None:
        return self.bot.get_guild(self.config["core"]["guild"])

    async def cog_load(self) -> None:
        self.db = await aiosqlite.connect(self.db_name)
        self.db.row_factory = aiosqlite.Row
        await self.db.execute("PRAGMA journal_mode=WAL;")

    async def cog_unload(self) -> None:
        if self.db:
            await self.db.close()

    async def add_user(self, user_id: int) -> bool:
        query = """
		INSERT OR IGNORE INTO users (id, level, xp_gained)
		VALUES (?, 1, 0);
		"""

        cursor = await self.db.execute(query, (user_id,))
        await self.db.commit()
        return cursor.rowcount > 0

    async def get_user(self, user_id: int) -> dict | None:
        self.db.row_factory = aiosqlite.Row
        async with self.db.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def add_xp(self, user_id: int, xp_amount: int) -> None:
        query = """
		INSERT INTO users (id, level, xp_gained)
		VALUES (?, 1, ?)
		ON CONFLICT(id) DO UPDATE SET
			xp_gained = users.xp_gained + excluded.xp_gained;
		"""

        await self.db.execute(query, (user_id, xp_amount))
        await self.db.commit()

    async def get_top_users(self, limit: int = 10) -> list:
        self.db.row_factory = aiosqlite.Row
        query = "SELECT id, level, xp_gained FROM users ORDER BY xp_gained DESC LIMIT ?"
        async with self.db.execute(query, (limit,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def record_message_if_new(self, message_id: int) -> bool:
        cursor = await self.db.execute(
            "INSERT OR IGNORE INTO messages (id) VALUES (?)", message_id
        )
        await self.db.commit()
        return cursor.rowcount > 0
