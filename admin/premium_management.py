from datetime import datetime, timedelta

from database.database import get_db


async def give_premium(user_id: int, days: int = 30):

    expire_date = (
        datetime.now() +
        timedelta(days=days)
    ).strftime("%Y-%m-%d %H:%M:%S")


    db = await get_db()

    await db.execute(
        """
        UPDATE users
        SET
            is_premium = 1,
            premium_expire_date = ?
        WHERE id = ?
        """,
        (
            expire_date,
            user_id
        )
    )

    await db.commit()
    await db.close()


async def remove_premium(user_id: int):

    db = await get_db()

    await db.execute(
        """
        UPDATE users
        SET
            is_premium = 0,
            premium_expire_date = NULL
        WHERE id = ?
        """,
        (user_id,)
    )

    await db.commit()
    await db.close()