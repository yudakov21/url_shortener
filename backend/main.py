from fastapi import FastAPI, status, Request, Body, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.database import engine
from db.models import Base
from services.service import ShortenerService
from core.exceptions import ShortenerBaseException
from dependencies import get_shortener_service


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


@app.exception_handler(ShortenerBaseException)
async def shortener_exception_handler(request: Request, exc: ShortenerBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.post("/")
async def genarate_short_url(long_url: str = Body(embed=True), 
                             shortener_service: ShortenerService = Depends(get_shortener_service)):
    slug = await shortener_service.get_or_generate_short_url(long_url=long_url)
    return {"data": slug}

@app.get("/{slug}")
async def redirect_to_long_url(slug: str, 
                               shortener_service: ShortenerService = Depends(get_shortener_service)):
    long_url = await shortener_service.get_url_by_slug(slug)
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)


