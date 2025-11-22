from database import new_session
from models import ShortURL
from sqlalchemy import select


async def add_slug_to_db(slug: str, long_url:str):
    async with new_session() as session:
        new_slug = ShortURL(slug=slug, long_url=long_url)
        session.add(new_slug)
        await session.commit()


async def get_slug_from_db(long_url: str):
    async with new_session() as session:
        query = select(ShortURL).where(ShortURL.long_url == long_url)
        result = await session.execute(query)
        row = result.scalar_one_or_none()

        return row.slug if row else None
    

async def get_long_url_by_slug(slug: str):
    async with new_session() as session:
        query = select(ShortURL).filter_by(slug = slug)
        result = await session.execute(query)
        row = result.scalar_one_or_none()
        
        return row.long_url if row else None
