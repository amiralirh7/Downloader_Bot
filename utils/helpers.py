import random

from database.database import get_db


def generate_user_id():

    return random.randint(
        1000000000,
        9999999999
    )