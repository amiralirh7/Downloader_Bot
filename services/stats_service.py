from database.database import get_db


async def get_stats():

    db = await get_db()

    users = await db.execute(
        "SELECT COUNT(*) FROM users"
    )

    total_users = await users.fetchone()


    premium = await db.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE is_premium = 1
        """
    )

    premium_users = await premium.fetchone()


    await db.close()


    return {
        "users": total_users[0],
        "premium": premium_users[0]
    }