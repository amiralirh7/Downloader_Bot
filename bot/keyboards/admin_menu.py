from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👥 مدیریت کاربران",
                    callback_data="manage_users"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💎 مدیریت پرمیوم",
                    callback_data="manage_premium"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢 مدیریت اسپانسر",
                    callback_data="manage_sponsors"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 آمار ربات",
                    callback_data="bot_stats"
                )
            ]
        ]
    )