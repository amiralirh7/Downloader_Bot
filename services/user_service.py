from datetime import datetime

from database.queries import (
    get_user_by_telegram_id,
    create_user
)

from database.database import get_db
from utils.helpers import generate_user_id


async def register_user(
    telegram_id: int,
    username: str | None,
    first_name: str
):

    existing_user = await get_user_by_telegram_id(
        telegram_id
    )

    if existing_user:
        return existing_user

    bot_user_id = generate_user_id()

    join_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    await create_user(
        bot_user_id=bot_user_id,
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        join_date=join_date
    )

    return await get_user_by_telegram_id(
        telegram_id
    )


async def is_user_banned(
    telegram_id: int
):

    db = await get_db()

    cursor = await db.execute(
        """
        SELECT telegram_id
        FROM banned_users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    result = await cursor.fetchone()

    await db.close()

    return result is not None


async def get_user(
    user_id: int
):

    db = await get_db()

    cursor = await db.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = await cursor.fetchone()

    await db.close()

    return user