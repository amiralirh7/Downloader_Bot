from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def profile_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💎 ارتقا به پرمیوم",
                    callback_data="premium"
                )
            ]
        ]
    )