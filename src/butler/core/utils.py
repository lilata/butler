from urllib.parse import urlparse


def is_url_valid(url: str) -> bool:
    if not isinstance(url, str):
        return False
    p = urlparse(url)
    return bool(p.scheme and p.netloc)
