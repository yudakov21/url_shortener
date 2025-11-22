from shortener import generate_random_slug
from db_manager import add_slug_to_db, get_slug_from_db, get_long_url_by_slug
from exceptions import NotLongUrlException


def normalize_url(long_url: str):
    if not long_url.startswith(("http://", "https://")):
        return "https://" + long_url
    return long_url


async def get_or_generate_short_url(long_url: str):
    long_url = normalize_url(long_url=long_url)

    slug = await get_slug_from_db(long_url=long_url)
    if slug:
        return slug
    
    slug = generate_random_slug()
    await add_slug_to_db(slug=slug, long_url=long_url)
    return slug


async def get_url_by_slug(slug: str) -> str:
    long_url = await get_long_url_by_slug(slug=slug)
    if not long_url:
        raise NotLongUrlException()
    return long_url
