import datetime
from typing import Type

from fastapi import Query
from sqlalchemy import func
from sqlalchemy.sql import Select

from APINews.db.base import Base


class QueryBuilder:
    def __init__(
        self,
        date_begin: datetime.date
        | None = Query(description="Дата парса от которой выбираем", default=None),
        date_end: datetime.date
        | None = Query(description="Дата парса до которой выбираем", default=None),
        publication_date_begin: int
        | None = Query(
            description="Дата и время публикации новости от которой выбираем",
            default=None,
        ),
        publication_date_end: int
        | None = Query(
            description="Дата и время публикации новости до которой выбираем",
            default=None,
        ),
        tag: str | None = Query(description="Тема новости", default=None),
        page: int | None = Query(description="Страниц", default=1),
        per_page: int
        | None = Query(description="Количество записей на странице", default=10),
    ):
        self.date_begin = date_begin
        self.date_end = date_end
        self.publication_date_begin = publication_date_begin
        self.publication_date_end = publication_date_end
        self.tag = tag
        self.page = page
        self.per_page = per_page

    def apply_filters(self, query: Select, table: Type["Base"]) -> Select:
        if self.date_begin:
            query = query.where(table.parse_date >= self.date_begin)

        if self.date_end:
            query = query.where(table.parse_date <= self.date_end)

        if self.publication_date_begin:
            query = query.where(table.publication_date >= self.publication_date_begin)

        if self.publication_date_end:
            query = query.where(table.publication_date <= self.publication_date_end)

        if self.tag:
            query = query.where(table.tag == self.tag)

        if self.page and self.per_page:
            query = query.add_columns(func.count("*").over().label("counting")).offset(
                self.per_page * (self.page - 1)
            ).limit(self.per_page)

        return query
