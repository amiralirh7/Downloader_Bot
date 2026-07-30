import asyncio
import time
from pathlib import Path

from aiogram.types import Message, FSInputFile

from utils.instagram_downloader import download_instagram


async def start_download(
    message: Message,
    url: str
):
    file_path = None

    try:
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