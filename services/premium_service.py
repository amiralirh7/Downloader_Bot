from datetime import datetime

from database.database import get_db


async def check_premium(user_id):

    db = await get_db()

    cursor = await db.execute(
        """
        SELECT is_premium, premium_expire_date
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = await cursor.fetchone()

    await db.close()

    if not user:
        return False

    is_premium, expire_date = user

    if not is_premium:
        return False

    if expire_date:
        expire = datetime.strptime(
            expire_date,
            "%Y-%m-%d %H:%M:%S"
        )

        if datetime.now() > expire:
            return False

    return True