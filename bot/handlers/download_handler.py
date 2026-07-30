from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.validators import is_instagram_url
from bot.messages.user_messages import SEND_INSTAGRAM_LINK
from bot.states.download_state import DownloadState
from bot.handlers.force_join_handler import send_force_join
from utils.download_service import start_download

router = Router()


@router.message(F.text == "📥 دانلود از اینستاگرام")
async def instagram_download_start(message: Message):
    await message.answer(SEND_INSTAGRAM_LINK)


@router.message(F.text.startswith("https://"))
@router.message(F.text.startswith("http://"))
async def receive_link(
    message: Message,
    state: FSMContext
):
    if not is_instagram_url(message.text):
        return

    await state.update_data(
        download_link=message.text
    )

    await state.set_state(
        DownloadState.waiting_for_join
    )

    joined = await send_force_join(message)

    if joined:
        return

    await start_download(
        message,
        message.text
    )