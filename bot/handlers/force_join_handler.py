from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from database.queries import get_all_sponsors
from bot.keyboards.force_join_menu import force_join_menu
from utils.download_service import start_download

router = Router()


async def check_force_join(bot, user_id):
    sponsors = await get_all_sponsors()

    if not sponsors:
        return True

    for sponsor in sponsors:
        username = sponsor[0]

        try:
            member = await bot.get_chat_member(
                chat_id=username,
                user_id=user_id
            )

            if member.status in ("left", "kicked"):
                return False

        except TelegramBadRequest:
            return False

    return True


async def send_force_join(message):
    sponsors = await get_all_sponsors()

    if not sponsors:
        return

    await message.answer(
        "📢 برای استفاده از ربات ابتدا در کانال‌های زیر عضو شوید و سپس روی «بررسی عضویت» بزنید.",
        reply_markup=force_join_menu(sponsors)
    )


@router.callback_query(F.data == "check_join")
async def check_join(
    callback: CallbackQuery,
    state: FSMContext
):
    if not await check_force_join(
        callback.bot,
        callback.from_user.id
    ):
        await callback.answer(
            "❌ هنوز عضو همه کانال‌ها نشده‌اید.",
            show_alert=True
        )
        return

    data = await state.get_data()
    link = data.get("download_link")

    await state.clear()
    await callback.message.delete()

    if link:
        await start_download(
            callback.message,
            link
        )
    else:
        await callback.message.answer(
            "✅ عضویت شما تایید شد."
        )