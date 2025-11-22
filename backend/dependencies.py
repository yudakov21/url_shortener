from fastapi import Depends
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from db_manager import DatabaseManager
from service import ShortenerService


async def get_db_manager(session: AsyncSession = Depends(get_async_session)):
    return DatabaseManager(session=session)

async def get_shortener_service(db_manager: DatabaseManager = Depends(get_db_manager)):
    return ShortenerService(db_manager=db_manager)