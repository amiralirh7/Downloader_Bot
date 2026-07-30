import os
import aiosqlite


DATABASE_NAME = os.path.join(
    "storage",
    "database",
    "bot.db"
)


async def get_db():

    return await aiosqlite.connect(
        DATABASE_NAME
    )


async def init_database():

    os.makedirs(
        os.path.dirname(DATABASE_NAME),
        exist_ok=True
    )

    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                bot_user_id INTEGER UNIQUE NOT NULL,

                telegram_id INTEGER UNIQUE NOT NULL,

                username TEXT,

                first_name TEXT,

                join_date TEXT,

                is_premium BOOLEAN DEFAULT 0,

                premium_expire_date TEXT,

                daily_download_count INTEGER DEFAULT 0,

                total_download_count INTEGER DEFAULT 0,

                status TEXT DEFAULT 'active'

            )
            """
        )


        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS admins (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                role TEXT NOT NULL

            )
            """
        )


        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS banned_users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                telegram_id INTEGER UNIQUE,

                reason TEXT,

                banned_date TEXT

            )
            """
        )


        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS sponsors (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                channel_username TEXT UNIQUE,

                is_active BOOLEAN DEFAULT 1

            )
            """
        )


        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS downloads (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                platform TEXT,

                content_type TEXT,

                download_date TEXT

            )
            """
        )


        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (

                key TEXT PRIMARY KEY,

                value TEXT

            )
            """
        )


        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS premium_payments (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                amount INTEGER,

                date TEXT,

                status TEXT

            )
            """
        )


        await db.commit()