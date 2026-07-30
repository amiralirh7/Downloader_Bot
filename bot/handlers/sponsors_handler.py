from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.keyboards.sponsors_menu import sponsors_menu

from config import OWNER_ID, ADMIN_1_ID, ADMIN_2_ID

from database.queries import (
    add_sponsor,
    remove_sponsor,
    get_all_sponsors
)

router = Router()


class SponsorManager(StatesGroup):
    waiting_for_channel = State()
    waiting_for_delete = State()


def is_admin(user_id: int):
    return user_id in (
        OWNER_ID,
        ADMIN_1_ID,
        ADMIN_2_ID
    )


@router.callback_query(F.data == "manage_sponsors")
async def manage_sponsors(
    callback: CallbackQuery,
    state: FSMContext
):
    if not is_admin(callback.from_user.id):
        await callback.answer(
            "دسترسی ندارید.",
            show_alert=True
        )
        return

    await state.clear()

    await callback.answer()

    await callback.message.answer(
         "📢 مدیریت اسپانسر",
        reply_markup=sponsors_menu()
    )

@router.callback_query(F.data == "add_sponsor")
async def add_sponsor_start(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.answer()

    await state.set_state(
        SponsorManager.waiting_for_channel
    )

    await callback.message.answer(
        "یوزرنیم کانال را ارسال کنید.\n\nمثال:\n@mychannel"
    )
    


@router.message(SponsorManager.waiting_for_channel)
async def add_sponsor_handler(
    message: Message,
    state: FSMContext
):
    channel = message.text.strip()

    await add_sponsor(channel)

    await state.clear()

    await message.answer(
        "✅ اسپانسر اضافه شد."
    )


@router.callback_query(F.data == "remove_sponsor")
async def remove_sponsor_start(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.answer()

    await state.set_state(
        SponsorManager.waiting_for_delete
    )

    await callback.message.answer(
        "یوزرنیم کانال را ارسال کنید."
    )


@router.message(SponsorManager.waiting_for_delete)
async def remove_sponsor_handler(
    message: Message,
    state: FSMContext
):
    channel = message.text.strip()

    await remove_sponsor(channel)

    await state.clear()

    await message.answer(
        "✅ اسپانسر حذف شد."
    )


@router.callback_query(F.data == "list_sponsors")
async def sponsors_list(
    callback: CallbackQuery
):
    await callback.answer()

    sponsors = await get_all_sponsors()

    if not sponsors:
        await callback.message.answer(
            "❌ هیچ اسپانسری ثبت نشده است."
        )
        return

    text = "📢 لیست اسپانسرها\n\n"

    for sponsor in sponsors:
        text += f"• {sponsor[0]}\n"

    await callback.message.answer(text)