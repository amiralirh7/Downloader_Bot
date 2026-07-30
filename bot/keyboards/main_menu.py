from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu(is_admin=False):

    buttons = [
        [
            KeyboardButton(text="👤 پروفایل"),
            KeyboardButton(text="💎 پرمیوم")
        ],
        [
            KeyboardButton(text="📥 دانلود از اینستاگرام")
        ]
    ]

    if is_admin:
        buttons.append(
            [
                KeyboardButton(text="🛠 پنل ادمین")
            ]
        )

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )