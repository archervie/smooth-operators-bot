# type: ignore

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

    @property
    def TIER_1(self) -> discord.Object:
        return discord.Object(self.config["roles"]["tier_1"])

    @property
    def TIER_2(self) -> discord.Object:
        return discord.Object(self.config["roles"]["tier_2"])

    @property
    def TIER_3(self) -> discord.Object:
        return discord.Object(self.config["roles"]["tier_3"])

    @staticmethod
    def get_xp_needed(level: int) -> int:
        return 50 * (level**2) + 50 * level

    @staticmethod
    def get_title_for_level(level: int) -> str:
        if level >= 20:
            return "Joestar"
        if level >= 15:
            return "Stand User"
        if level >= 10:
            return "Hamon User"
        return "Subscriber"

    async def cog_load(self) -> None:
        self.db = await aiosqlite.connect(self.db_name)
        self.db.row_factory = aiosqlite.Row

    async def cog_unload(self) -> None:
        if self.db:
            await self.db.close()

    async def add_user_to_db(self, user_id: int) -> bool:
        query = """
		INSERT OR IGNORE INTO users (id, level, xp_gained)
		VALUES (?, 1, 0);
		"""

        cursor = await self.db.execute(query, (user_id,))
        await self.db.commit()
        return cursor.rowcount > 0

    async def get_user_from_db(self, user_id: int) -> dict | None:
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

    async def set_user_title(self, user_id: int, new_title: str) -> bool:
        cursor = await self.db.execute(
            "UPDATE users SET title = ? WHERE id = ?", (new_title, user_id)
        )
        await self.db.commit()
        return cursor.rowcount > 0

    async def check_and_apply_level_up(self, user_id: int) -> dict | None:
        user = await self.get_user_from_db(user_id)
        if not user:
            return None

        current_level = user["level"]
        current_xp = user["xp_gained"]
        old_title = self.get_title_for_level(current_level)
        starting_level = current_level

        while True:
            xp_needed = self.get_xp_needed(current_level)
            if current_xp >= xp_needed:
                current_xp -= xp_needed
                current_level += 1
            else:
                break

        if current_level == starting_level:
            return None

        new_title = self.get_title_for_level(current_level)

        query = """
			UPDATE users
			SET level = ?, xp_gained = ?, title = ?
			WHERE id = ?;
			"""
        await self.db.execute(query, (current_level, current_xp, new_title, user_id))
        await self.db.commit()

        return {
            "old_level": starting_level,
            "new_level": current_level,
            "old_title": old_title,
            "new_title": new_title,
            "xp_remaining": current_xp,
            "xp_next_level": self.get_xp_needed(current_level),
        }
