from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from services.user_service import register_user, is_user_banned
from bot.keyboards.main_menu import main_menu
from bot.messages.user_messages import WELCOME_MESSAGE
from bot.handlers.admin_handler import is_admin


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):

    telegram_id = message.from_user.id

    if await is_user_banned(telegram_id):
        await message.answer(
            "❌ شما اجازه استفاده از ربات را ندارید."
        )
        return

    await register_user(
        telegram_id=telegram_id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )

    await message.answer(
        WELCOME_MESSAGE,
        reply_markup=main_menu(
            is_admin=is_admin(message.from_user.id)
        )
    )