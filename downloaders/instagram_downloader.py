from downloaders.base_downloader import BaseDownloader


class InstagramDownloader(BaseDownloader):

    async def download(self, url: str):

        # TODO:
        # منطق دانلود اینستاگرام بعداً اضافه می‌شود

        return {
            "status": "success",
            "platform": "instagram",
            "url": url
        }