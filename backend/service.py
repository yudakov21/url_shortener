from urllib.parse import urlparse
from fastapi import HTTPException, status


from shortener import generate_random_slug
from db_manager import DatabaseManager
from exceptions import NotLongUrlException


class ShortenerService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def normalize_url(self, long_url: str) -> str:
        long_url = long_url.strip()

        if not long_url or len(long_url) < 30:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL cannot be empty or shorter than 30 chars")
        
        parsed = urlparse(long_url)
        if not parsed.scheme or not parsed.netloc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL format")
        
        return long_url


    async def generate_unique_slug(self, attempts: int = 10) -> str:
        for _ in range(attempts):
            slug = generate_random_slug()

            if not await self.db_manager.slug_exists(slug=slug):
                return slug
            
        raise RuntimeError("Unable to generate unique slug after 10 attempts")
        

    async def get_or_generate_short_url(self, long_url: str) -> str:
        long_url = self.normalize_url(long_url=long_url)

        slug = await self.db_manager.get_slug_from_db(long_url=long_url)
        if slug:
            return slug
        
        slug = await self.generate_unique_slug()
        await self.db_manager.add_slug_to_db(slug=slug, long_url=long_url)
        return slug


    async def get_url_by_slug(self, slug: str) -> str:
        long_url = await self.db_manager.get_long_url_by_slug(slug=slug)
        if not long_url:
            raise NotLongUrlException()
        return long_url
