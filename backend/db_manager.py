from models import ShortURL
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_slug_to_db(self, slug: str, long_url:str):
        new_slug = ShortURL(slug=slug, long_url=long_url)
        self.session.add(new_slug)
        await self.session.commit()

    async def get_slug_from_db(self, long_url: str):
        query = select(ShortURL).where(ShortURL.long_url == long_url)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()

        return row.slug if row else None
        

    async def get_long_url_by_slug(self, slug: str):
        query = select(ShortURL).filter_by(slug = slug)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        
        return row.long_url if row else None
