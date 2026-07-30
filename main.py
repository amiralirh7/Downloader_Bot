import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from database.database import init_database
from bot import register_routers


async def main():

    await init_database()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher()

    register_routers(dp)

    print("🤖 Downloader Bot Started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())