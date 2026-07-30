from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import OWNER_ID, ADMIN_1_ID, ADMIN_2_ID

# این توابع بعداً داخل database/queries.py ساخته می‌شوند
from database.queries import (
    get_user_by_telegram_id,
    get_user_by_username,
    ban_user,
    unban_user,
    activate_premium,
    remove_premium,
    delete_user
)

router = Router()


class UserManager(StatesGroup):
    waiting_for_user_id = State()


def is_admin(user_id: int):
    return user_id in (
        OWNER_ID,
        ADMIN_1_ID,
        ADMIN_2_ID
    )


@router.callback_query(F.data == "manage_users")
async def manage_users(
    callback: CallbackQuery,
    state: FSMContext
):
    

    if not is_admin(callback.from_user.id):
        await callback.answer(
            "دسترسی ندارید.",
            show_alert=True
        )
        return

    await callback.answer()

    await state.set_state(
        UserManager.waiting_for_user_id
    )

    await callback.message.answer(
    "🆔 Telegram ID یا Username کاربر را ارسال کنید.\n\nمثال:\n123456789\nیا\n@amir"
    )
@router.message(UserManager.waiting_for_user_id)
async def receive_user_id(
    message: Message,
    state: FSMContext
):

    search = message.text.strip()

    if search.isdigit():
        telegram_id = int(search)

        user = await get_user_by_telegram_id(
            telegram_id
        )

    else:
        username = search.replace("@", "")

        user = await get_user_by_username(
            username
        )

    if not user:
        await message.answer(
            "❌ کاربری با این Telegram ID پیدا نشد."
        )
        return

    await state.clear()

    # ترتیب فیلدها مطابق جدول users
    bot_user_id = user[1]
    telegram_id = user[2]
    username = user[3] or "-"
    first_name = user[4]
    join_date = user[5]

    is_premium = "✅ پرمیوم" if user[6] else "❌ عادی"

    premium_expire = (
        user[7]
        if user[7]
        else "-"
    )

    today_downloads = user[8]
    total_downloads = user[9]

    status = user[10]

    text = (
        "👤 اطلاعات کاربر\n\n"

        f"🆔 شناسه ربات: {bot_user_id}\n"
        f"📱 Telegram ID: {telegram_id}\n"
        f"👤 نام: {first_name}\n"
        f"🔗 یوزرنیم: @{username}\n"
        f"📅 تاریخ عضویت: {join_date}\n\n"

        f"📥 دانلود امروز: {today_downloads}/20\n"
        f"📦 کل دانلودها: {total_downloads}\n\n"

        f"💎 سطح: {is_premium}\n"
        f"⏳ پایان اشتراک: {premium_expire}\n\n"

        f"🚫 وضعیت: {status}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="⭐ فعال‌سازی پرمیوم",
                    callback_data=f"premium_on:{telegram_id}"
                ),
                InlineKeyboardButton(
                    text="❌ حذف پرمیوم",
                    callback_data=f"premium_off:{telegram_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🚫 بن کاربر",
                    callback_data=f"ban:{telegram_id}"
                ),
                InlineKeyboardButton(
                    text="✅ رفع بن",
                    callback_data=f"unban:{telegram_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🔄 بروزرسانی",
                    callback_data=f"refresh:{telegram_id}"
                ),
                InlineKeyboardButton(
                    text="🗑 حذف کامل",
                    callback_data=f"delete:{telegram_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🔙 بازگشت",
                    callback_data="back_admin"
                )
            ]
        ]
    )

    await message.answer(
        text,
        reply_markup=keyboard
    )
@router.callback_query(F.data.startswith("premium_on:"))
async def premium_on(
    callback: CallbackQuery
):

    telegram_id = int(
        callback.data.split(":")[1]
    )

    await activate_premium(
        telegram_id
    )

    await callback.answer(
        "✅ پرمیوم فعال شد"
    )


@router.callback_query(F.data.startswith("premium_off:"))
async def premium_off(
    callback: CallbackQuery
):

    telegram_id = int(
        callback.data.split(":")[1]
    )

    await remove_premium(
        telegram_id
    )

    await callback.answer(
        "❌ پرمیوم حذف شد"
    )


@router.callback_query(F.data.startswith("ban:"))
async def ban_handler(
    callback: CallbackQuery
):

    telegram_id = int(
        callback.data.split(":")[1]
    )

    await ban_user(
        telegram_id
    )

    await callback.answer(
        "🚫 کاربر بن شد"
    )


@router.callback_query(F.data.startswith("unban:"))
async def unban_handler(
    callback: CallbackQuery
):

    telegram_id = int(
        callback.data.split(":")[1]
    )

    await unban_user(
        telegram_id
    )

    await callback.answer(
        "✅ کاربر آنبن شد"
    )


@router.callback_query(F.data.startswith("delete:"))
async def delete_handler(
    callback: CallbackQuery
):

    telegram_id = int(
        callback.data.split(":")[1]
    )

    await delete_user(
        telegram_id
    )

    await callback.answer(
        "🗑 کاربر حذف شد"
    )

    await callback.message.edit_text(
        "✅ اطلاعات کاربر به طور کامل حذف شد."
    )


@router.callback_query(F.data.startswith("refresh:"))
async def refresh_handler(
    callback: CallbackQuery
):

    telegram_id = int(
        callback.data.split(":")[1]
    )

    user = await get_user_by_telegram_id(
        telegram_id
    )

    if not user:
        await callback.answer(
            "❌ کاربر وجود ندارد",
            show_alert=True
        )
        return

    await callback.answer(
        "🔄 اطلاعات بروزرسانی شد"
    )

    await callback.message.answer(
        "برای مشاهده اطلاعات جدید، دوباره Telegram ID را ارسال کنید."
    )


@router.callback_query(F.data == "back_admin")
async def back_admin(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.clear()

    await callback.answer()

    await callback.message.delete()