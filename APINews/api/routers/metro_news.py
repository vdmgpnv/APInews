import datetime

from fastapi import APIRouter, Depends, Query
from dateutil.relativedelta import relativedelta
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from APINews.api.query_builder import QueryBuilder
from APINews.db.base import get_db_session
from APINews.db.models.public import News
from APINews.api.models.news import BaseNews, NewsExtended

metro_router = APIRouter(prefix="/news", tags=["metro"])


@metro_router.get(
    "/metro",
    description="Возвращает новости спаршенные за последние day дней",
    response_model=list[BaseNews],
)
async def get_metro_news(
    day: int = Query(
        default=5, description="Количество дней, за которые мы хотим получить новости"
    ),
    session: AsyncSession = Depends(get_db_session),
):
    date_end = datetime.date.today()
    date_begin = date_end - relativedelta(days=day)

    query = (
        select(
            News.header,
            func.to_char(func.to_timestamp(News.publication_date), "YYYY-MM-DD").label(
                "publication_date"
            ),
            News.image_url,
        )
        .select_from(News)
        .where(News.parse_date.between(date_begin, date_end))
    )

    result = await session.execute(query)
    data = result.mappings().all()

    return data


@metro_router.get(
    "/news-extended",
    description="Версия апишки, но с фмльтрами",
    response_model=list[NewsExtended],
)
async def get_news_extended(
    query_builder: QueryBuilder = Depends(QueryBuilder),
    session: AsyncSession = Depends(get_db_session),
):
    query = (
        select(
            News.header,
            func.to_char(func.to_timestamp(News.publication_date), "YYYY-MM-DD").label(
                "publication_date"
            ),
            News.image_url,
            News.page_link
        )
        .select_from(News)
    )

    query_with_filters = query_builder.apply_filters(query, News)

    result = await session.execute(query_with_filters)
    data = result.mappings().all()

    return data
