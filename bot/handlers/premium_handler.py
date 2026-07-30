from aiogram import Router, F
from aiogram.types import Message

from bot.messages.user_messages import PREMIUM_MESSAGE


router = Router()


@router.message(F.text == "💎 پرمیوم")
async def premium_handler(message: Message):

    await message.answer(
        PREMIUM_MESSAGE
    )