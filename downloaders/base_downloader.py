from abc import ABC, abstractmethod


class BaseDownloader(ABC):

    @abstractmethod
    async def download(self, url: str):
        pass