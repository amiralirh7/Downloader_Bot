from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def sponsors_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ افزودن اسپانسر",
                    callback_data="add_sponsor"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ حذف اسپانسر",
                    callback_data="remove_sponsor"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 لیست اسپانسرها",
                    callback_data="list_sponsors"
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