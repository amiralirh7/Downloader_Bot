from database.database import get_db


async def delete_user(telegram_id: int):

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

    if not user:
        await db.close()
        return False

    user_id = user[0]

    await db.execute(
        """
        DELETE FROM downloads
        WHERE user_id = ?
        """,
        (user_id,)
    )

    await db.execute(
        """
        DELETE FROM premium_payments
        WHERE user_id = ?
        """,
        (user_id,)
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
        INSERT OR REPLACE INTO banned_users
        (
            telegram_id,
            reason,
            banned_date
        )
        VALUES
        (
            ?,
            '',
            datetime('now')
        )
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()

    return True


async def unban_user(telegram_id: int):

    db = await get_db()

    await db.execute(
        """
        DELETE FROM banned_users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    await db.commit()
    await db.close()

    return True