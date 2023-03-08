from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from APINews.api.routers.metro_news import metro_router

app = FastAPI(
    title="MoscowNews",
    version="0.1Alpha",
    description="Сервис получения новостей Москвы",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metro_router)



