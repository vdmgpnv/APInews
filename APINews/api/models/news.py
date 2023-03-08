import datetime

from pydantic import BaseModel, Field


class BaseNews(BaseModel):
    header: str
    publication_date: datetime.date = Field(alias="publicationDate")
    image_url: str | None = Field(alias="imageUrl")

    class Config:
        allow_population_by_field_name = True


class NewsExtended(BaseNews):
    page_link: str = Field(alias="pageLink")

