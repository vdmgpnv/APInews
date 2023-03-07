from typing import Any, Type
from sqlalchemy.dialects.postgresql import insert

from APINews.db.base import Base, DBSession
from parser.request_client import RequestClient
from utils.exceptions import NoDataError
from utils.logger import logger


class BaseParser:
    def __init__(self, base_url: str, model: Type["Base"]):
        self.base_url = base_url
        self.client = RequestClient(base_url)
        self.session = DBSession()
        self.model = model

    async def parse(self, path: str, mode: str):
        logger.info(f"Start parse {self.base_url + path}")
        raw_data = await self.client.request(url=path, mode=mode)
        if not raw_data:
            raise NoDataError()
        logger.info("Parse complete, start process data")
        processed_data = await self.process_data(raw_data)
        logger.info(f"Processing completed, start save {len(processed_data)}, saving...")
        await self.save_data(processed_data)
        logger.info("Successfully saved data")

    async def process_data(self, data: dict[str, Any] | str) -> list[dict[str, Any]]:
        raise NotImplementedError

    async def save_data(self, data: list[dict[str, Any]]) -> None:
        insert_statement = insert(self.model).values(data)
        async with self.session as session:
            await session.execute(
                insert_statement.on_conflict_do_update(
                    index_elements=(self.model.publication_date, self.model.header),
                    set_={"parse_date": insert_statement.excluded.parse_date},
                )
            )
