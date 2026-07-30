from dataclasses import dataclass


@dataclass
class User:
    id: int
    telegram_id: int
    username: str | None
    first_name: str
    join_date: str
    is_premium: bool
    premium_expire_date: str | None
    daily_download_count: int
    total_download_count: int
    status: str