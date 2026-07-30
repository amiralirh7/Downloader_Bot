from database.database import get_db


async def get_active_sponsors():

    db = await get_db()

    cursor = await db.execute(
        """
        SELECT channel_username
        FROM sponsors
        WHERE is_active = 1
        """
    )

    sponsors = await cursor.fetchall()

    await db.close()

    return [
        sponsor[0]
        for sponsor in sponsors
    ]


async def add_sponsor(channel_username):

    db = await get_db()

    await db.execute(
        """
        INSERT INTO sponsors(channel_username)
        VALUES(?)
        """,
        (channel_username,)
    )

    await db.commit()
    await db.close()