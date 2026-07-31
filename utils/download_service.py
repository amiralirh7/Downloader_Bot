import asyncio
import time
from pathlib import Path

from aiogram.types import Message, FSInputFile
from config import DAILY_DOWNLOAD_LIMIT
from database.queries import get_user_by_telegram_id

from utils.instagram_downloader import download_instagram
from database.queries import (
    get_daily_download_count,
    increase_daily_download,
    increase_total_download
)


async def start_download(
    message: Message,
    url: str
):
    file_path = None

    try:
        user = await get_user_by_telegram_id(
            message.from_user.id
)

        if not user:
            return

        is_premium = user[6]

        if not is_premium:
            daily_count = await get_daily_download_count(
                message.from_user.id
            )

            if daily_count >= DAILY_DOWNLOAD_LIMIT:
                await message.answer(
                    "❌ سقف دانلود روزانه شما به پایان رسیده است."
                )
                return

        await message.answer("⏳ در حال دانلود...")

        t1 = time.time()

        file_path = await download_instagram(url)

        print(
            f"Download Time: {time.time() - t1:.2f} sec"
        )

        t2 = time.time()

        await message.answer_document(
            document=FSInputFile(file_path),
            request_timeout=300
        )

        print(
            f"Upload Time: {time.time() - t2:.2f} sec"
        )

        await increase_daily_download(
            message.from_user.id
        )

        await increase_total_download(
            message.from_user.id
        )

    finally:
        if file_path:
            await asyncio.sleep(60)

            try:
                Path(file_path).unlink(
                    missing_ok=True
                )

                print(
                    f"Deleted: {file_path}"
                )

            except Exception as e:
                print(
                    f"Delete Error: {e}"
                )