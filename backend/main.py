from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import engine
from models import Base
from service import get_or_generate_short_url, get_url_by_slug
from exceptions import NotLongUrlException


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    

app = FastAPI(lifespan=lifespan)


app.add_middleware(    
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def genarate_short_url(long_url: str = Body(embed=True)):
    slug = await get_or_generate_short_url(long_url=long_url)
    return {"data": slug}

@app.get("/{slug}")
async def redirect_to_long_url(slug: str):
    try:
        long_url = await get_url_by_slug(slug)
    except NotLongUrlException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Url was not found!!!")
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)


