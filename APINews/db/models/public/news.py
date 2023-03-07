import datetime

from sqlalchemy import Column, Date, Integer, String, Text, UniqueConstraint

from APINews.db.base import Base


class News(Base):
    __tablename__ = "news"
    __table_args__ = (
        UniqueConstraint("publication_date", "header", name="news_unique"),
        {"schema": "public"},
    )

    id: int = Column("id", Integer, index=True, autoincrement=True, primary_key=True)
    parse_date: datetime.date = Column("parse_date", Date, nullable=False)
    publication_date: int = Column("publication_date", Integer, index=True)
    header: str = Column("header", String, nullable=False)
    image_url: str = Column("image_url", Text, default=None, nullable=True)
    page_link: str = Column("page_link", Text, nullable=False)
