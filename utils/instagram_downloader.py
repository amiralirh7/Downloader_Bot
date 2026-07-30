from pathlib import Path
import yt_dlp

BASE_DIR = Path(__file__).resolve().parent.parent

DOWNLOAD_DIR = BASE_DIR / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

FFMPEG_DIR = BASE_DIR / "ffmpeg"


async def download_instagram(url: str):

    ydl_opts = {
        "outtmpl": str(DOWNLOAD_DIR / "%(id)s.%(ext)s"),
        "format": "best",
        "merge_output_format": "mp4",
        "ffmpeg_location": str(FFMPEG_DIR),
        "quiet": True,
        "noplaylist": True,
        "retries": 10,
        "fragment_retries": 10,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            url,
            download=True
        )

        file_path = Path(
            ydl.prepare_filename(info)
        )

    return file_path