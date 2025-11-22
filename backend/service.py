from shortener import generate_random_slug
from db_manager import DatabaseManager
from exceptions import NotLongUrlException


class ShortenerService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def normalize_url(self, long_url: str):
        if not long_url.startswith(("http://", "https://")):
            return "https://" + long_url
        return long_url


    async def get_or_generate_short_url(self, long_url: str):
        long_url = self.normalize_url(long_url=long_url)

        slug = await self.db_manager.get_slug_from_db(long_url=long_url)
        if slug:
            return slug
        
        slug = generate_random_slug()
        await self.db_manager.add_slug_to_db(slug=slug, long_url=long_url)
        return slug


    async def get_url_by_slug(self, slug: str) -> str:
        long_url = await self.db_manager.get_long_url_by_slug(slug=slug)
        if not long_url:
            raise NotLongUrlException()
        return long_url
