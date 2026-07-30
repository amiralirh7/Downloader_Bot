from aiogram import Router, F
from aiogram.types import Message

from database.queries import get_user_by_telegram_id
from bot.messages.user_messages import PROFILE_MESSAGE
from config import DEFAULT_DAILY_LIMIT


router = Router()


@router.message(F.text == "👤 پروفایل")
async def profile_handler(message: Message):

    user = await get_user_by_telegram_id(
        message.from_user.id
    )


    if not user:
        await message.answer(
            "❌ کاربر پیدا نشد."
        )
        return


    level = "💎 پرمیوم" if user[5] else "⭐ عادی"


    text = PROFILE_MESSAGE.format(
        user_id=user[0],
        name=user[4],
        join_date=user[5],
        level=level,
        today_downloads=user[7],
        daily_limit=DEFAULT_DAILY_LIMIT,
        total_downloads=user[8]
    )


    await message.answer(text)