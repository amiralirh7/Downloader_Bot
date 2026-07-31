from database.database import get_db


async def get_user_by_telegram_id(telegram_id: int):

    db = await get_db()

    cursor = await db.execute(
        """
        SELECT *
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    user = await cursor.fetchone()

    await db.close()

    return user


async def get_user_by_username(username: str):
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = await cursor.fetchone()

    await db.close()

    return user


async def create_user(
    bot_user_id: int,
    telegram_id: int,
    username: str | None,
    first_name: str,
    join_date: str
):

    db = await get_db()

    await db.execute(
        """
        INSERT INTO users
        (
            bot_user_id,
            telegram_id,
            username,
            first_name,
            join_date
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            bot_user_id,
            telegram_id,
            username,
            first_name,
            join_date
        )
    )

    await db.commit()
    await db.close()


async def ban_user(telegram_id: int):

    db = await get_db()

    await db.execute(
        """
        UPDATE users
        SET status = 'banned'
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.execute(
        """
        INSERT OR REPLACE INTO banned_users
        (
            telegram_id,
            reason,
            banned_date
        )
        VALUES (?, ?, datetime('now'))
        """,
        (
            telegram_id,
            "Banned by admin"
        )
    )

    await db.commit()
    await db.close()


async def unban_user(telegram_id: int):

    db = await get_db()

    await db.execute(
        """
        UPDATE users
        SET status = 'active'
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.execute(
        """
        DELETE FROM banned_users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()


async def activate_premium(telegram_id: int):

    db = await get_db()

    await db.execute(
        """
        UPDATE users
        SET
            is_premium = 1,
            premium_expire_date = datetime('now', '+30 days')
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()


async def remove_premium(telegram_id: int):

    db = await get_db()

    await db.execute(
        """
        UPDATE users
        SET
            is_premium = 0,
            premium_expire_date = NULL
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()


async def delete_user(telegram_id: int):

    db = await get_db()

    await db.execute(
        """
        DELETE FROM downloads
        WHERE user_id IN (
            SELECT id
            FROM users
            WHERE telegram_id = ?
        )
        """,
        (telegram_id,)
    )

    await db.execute(
        """
        DELETE FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.execute(
        """
        DELETE FROM banned_users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()


async def get_users_count():

    db = await get_db()

    cursor = await db.execute(
        """
        SELECT COUNT(*)
        FROM users
        """
    )

    result = await cursor.fetchone()

    await db.close()

    return result[0]


async def get_premium_users_count():

    db = await get_db()

    cursor = await db.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE is_premium = 1
        """
    )


async def add_sponsor(channel_username: str):
    db = await get_db()

    await db.execute(
        """
        INSERT OR IGNORE INTO sponsors
        (
            channel_username
        )
        VALUES (?)
        """,
        (channel_username,)
    )

    await db.commit()
    await db.close()


async def remove_sponsor(channel_username: str):
    db = await get_db()

    await db.execute(
        """
        DELETE FROM sponsors
        WHERE channel_username = ?
        """,
        (channel_username,)
    )

    await db.commit()
    await db.close()


async def get_all_sponsors():
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT channel_username
        FROM sponsors
        WHERE is_active = 1
        ORDER BY id DESC
        """
    )

    sponsors = await cursor.fetchall()

    await db.close()

    return sponsors


async def increase_daily_download(telegram_id: int):
    db = await get_db()

    await db.execute(
        """
        UPDATE users
        SET daily_download_count = daily_download_count + 1
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()


async def increase_total_download(telegram_id: int):
    db = await get_db()

    await db.execute(
        """
        UPDATE users
        SET total_download_count = total_download_count + 1
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()


async def get_daily_download_count(telegram_id: int):
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT daily_download_count
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    result = await cursor.fetchone()

    await db.close()

    if result:
        return result[0]

    return 0


async def reset_daily_downloads():
    db = await get_db()

    await db.execute(
        """
        UPDATE users
        SET daily_download_count = 0
        """
    )

    await db.commit()
    await db.close()


 