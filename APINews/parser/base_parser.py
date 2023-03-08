from typing import Any, Type
from sqlalchemy.dialects.postgresql import insert

from APINews.db.base import Base, DBSession
from APINews.parser.request_client import RequestClient
from utils.exceptions import NoDataError
from utils.logger import logger


class BaseParser:
    """Базовый класс парсера, принимающий сайт, который парсим,
    модель таблицы, в которую будут вставляться данные
    а так же тэг, который отображает смысл новости(метро, дороги и тд)
    """
    def __init__(self, base_url: str, model: Type["Base"], tag: str):
        self.base_url = base_url
        self.tag = tag
        self.client = RequestClient(base_url)
        self.session = DBSession()
        self.model = model

    async def parse(self, path: str, mode: str):
        """Основная функция, которая запускает парс, принимает путь запроса и мод,
         в котором ожидается ответ от сервера"""
        logger.info(f"Start parse {self.base_url + path}")
        raw_data = await self.client.request(url=path, mode=mode)
        if not raw_data:
            raise NoDataError()
        logger.info("Parse complete, start process data")
        processed_data = await self.process_data(raw_data)
        logger.info(f"Processing completed, start save {len(processed_data)}, saving...")
        await self.save_data(processed_data)
        logger.info("Successfully saved data")
        return

    async def process_data(self, data: dict[str, Any] | str) -> list[dict[str, Any]]:
        """Функция обработки спаршенных данных, необходимо переопределиять"""
        raise NotImplementedError

    async def save_data(self, data: list[dict[str, Any]]) -> None:
        """Метод сохранения в базу"""
        insert_statement = insert(self.model).values(data)
        async with self.session as session:
            await session.execute(
                insert_statement.on_conflict_do_update(
                    index_elements=(self.model.publication_date, self.model.header),
                    set_={"parse_date": insert_statement.excluded.parse_date},
                )
            )
        self.session.close() # без этой строчки не работает в качестве периодической таски
