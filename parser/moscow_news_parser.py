import datetime
import re
from typing import Any, Union

from bs4 import BeautifulSoup, Tag

from parser.base_parser import BaseParser
from utils.logger import logger


class MoscowNewsParser(BaseParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process_data(self, data: dict[str, Any] | str) -> list[dict[str, Any]]:
        output_data = []
        soup = BeautifulSoup(data, "html.parser")
        news_tables = soup.find_all("table", {"width": "95%"})
        for table in news_tables:
            news = table.contents
            for publication in news:
                if isinstance(publication, Tag):
                    prepared_row = await self.prepare_row_for_insert(
                        list(publication.children)
                    )
                    if prepared_row and not any(
                        row["header"] == prepared_row["header"]
                        and row["publication_date"]
                        == prepared_row["publication_date"]
                        for row in output_data
                    ):
                        output_data.append(prepared_row)
        return output_data

    async def prepare_row_for_insert(
        self, row: list[Tag]
    ) -> dict[str, Union[datetime.datetime, datetime.date, str]] | None:
        try:
            parse_date = datetime.date.today()
            raw_publication_date = re.findall(
                r"\d\d.\d\d.\d\d\d\d \d\d:\d\d", row[1].contents[0].text
            )[0]
            publication_date = int(
                datetime.datetime.strptime(
                    raw_publication_date, "%d.%m.%Y %H:%M"
                ).strftime("%s")
            )
            header = (
                list(row[1].children)[0].find_all_next("font", {"size": "3"})[0].text
            )
            page_link = None
            image_url = None
            try:
                page_link = (
                    self.client.base_url + list(row[0].children)[0].attrs["href"]
                )
            except IndexError:
                page_link = (
                    self.client.base_url
                    + list(row[1].children)[0].find_all_next("a")[0]["href"]
                )
            try:
                image_url = (
                    self.client.base_url
                    + list(row[0].children)[0].find_all_next("img")[0].attrs["src"]
                )
            except IndexError:
                pass

            prepared_row = dict(
                parse_date=parse_date,
                publication_date=publication_date,
                header=header,
                image_url=image_url,
                page_link=page_link,
            )
            return prepared_row

        except Exception as e:
            logger.error(f"{e}")
            return
