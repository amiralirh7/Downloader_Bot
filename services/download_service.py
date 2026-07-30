from database.database import get_db


async def can_download(
    telegram_id: int,
    limit: int = 20
):
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

    if result is None:
        return False

    return result[0] < limit


async def increase_download_count(
    telegram_id: int,
    content_type: str,
    platform: str
):
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT id
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    user = await cursor.fetchone()

    if user is None:
        await db.close()
        return

    user_id = user[0]

    await db.execute(
        """
        UPDATE users
        SET
            daily_download_count = daily_download_count + 1,
            total_download_count = total_download_count + 1
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.execute(
        """
        INSERT INTO downloads
        (
            user_id,
            platform,
            content_type,
            download_date
        )
        VALUES (?, ?, ?, datetime('now'))
        """,
        (
            user_id,
            platform,
            content_type
        )
    )

    await db.commit()
    await db.close()