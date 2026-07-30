import os

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = int(os.getenv("OWNER_ID", 0))
ADMIN_1_ID = int(os.getenv("ADMIN_1_ID", 0))
ADMIN_2_ID = int(os.getenv("ADMIN_2_ID", 0))


DATABASE_NAME = "database.db"


DEFAULT_DAILY_LIMIT = 20


BOT_NAME = "DownloaderBot"


PREMIUM_PRICE = 0