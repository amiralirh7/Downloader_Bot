from database.database import get_db


async def add_sponsor(channel_username: str):

    db = await get_db()

    await db.execute(
        """
        INSERT INTO sponsors
        (
            channel_username
        )
        VALUES
        (
            ?
        )
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


async def get_sponsors():

    db = await get_db()

    cursor = await db.execute(
        """
        SELECT channel_username
        FROM sponsors
        """
    )

    data = await cursor.fetchall()

    await db.close()

    return data