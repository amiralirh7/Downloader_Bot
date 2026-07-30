from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.keyboards.admin_menu import admin_menu
from bot.messages.admin_messages import ADMIN_PANEL_MESSAGE

from config import OWNER_ID, ADMIN_1_ID, ADMIN_2_ID


router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in (
        OWNER_ID,
        ADMIN_1_ID,
        ADMIN_2_ID
    )


@router.message(F.text == "🛠 پنل ادمین")
async def admin_panel(message: Message):

    

    if not is_admin(message.from_user.id):
        await message.answer(
            "❌ دسترسی ندارید."
        )
        return

    await message.answer(
        ADMIN_PANEL_MESSAGE,
        reply_markup=admin_menu()
    )


