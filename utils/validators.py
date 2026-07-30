import re


def is_instagram_url(url: str) -> bool:
    pattern = r"(https?://)?(www\.)?instagram\.com/"

    return bool(
        re.match(pattern, url)
    )