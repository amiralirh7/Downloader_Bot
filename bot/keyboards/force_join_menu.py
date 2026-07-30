from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def force_join_menu(sponsors):
    keyboard = []

    for sponsor in sponsors:
        username = sponsor[0]

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"📢 {username}",
                    url=f"https://t.me/{username.replace('@', '')}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="✅ بررسی عضویت",
                callback_data="check_join"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )