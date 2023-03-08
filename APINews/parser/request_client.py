import asyncio
from typing import Any, Union
from httpx import AsyncClient, Cookies, HTTPError

from utils.constants import REQUEST_TIMEOUT
from utils.logger import logger


class RequestClient:
    """Клиент для создания запросов, принимает базовую урлу, может быть расширен"""
    def __init__(self, base_url: str):
        self.base_url: str = base_url
        self.session: AsyncClient = AsyncClient()
        self.cookies = None

    async def __request(
        self,
        method: str,
        url: str,
        body: [dict[str, Any]] = None,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        mode: str = "json",
        retries: int = 3,
    ) -> Union[dict[str, Any], str, Cookies, bytes, None]:
        """Функция выполняющая запрос к серверу, в зависимости
         от переданного ей мода, вернет данные в разных форматах
         При написании функции преследовалась цель сделать ее как можно более универсальной
         """
        attempts = 1
        while attempts < retries:
            try:
                response = await self.session.request(
                    method,
                    url,
                    params=params,
                    json=body,
                    headers=headers,
                    timeout=REQUEST_TIMEOUT,
                )

                response.raise_for_status()

                match mode:
                    case "json":
                        return response.json()
                    case "text":
                        return response.text
                    case "cookies":
                        return response.cookies
                    case "binary":
                        return response.read()
                    case "headers":
                        return response.headers
                    case _:
                        logger.error("The bad response mode given")
                        return

            except HTTPError as exc:
                logger.error(
                    f"Exception during getting data from url {url} in {attempts} of {retries} attemtps"
                )

                if attempts == retries:
                    logger.error(f"Could not get data from {url}")

                attempts += 1
                await asyncio.sleep(1)

    async def request(
        self,
        url: str,
        method: str = "GET",
        body: [dict[str, Any]] = None,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        mode: str = "json",
        retries: int = 3,
    ) -> Union[dict[str, Any], str, Cookies, bytes, None]:
        url_for_request = self.base_url + url
        return await self.__request(
            method,
            url_for_request,
            headers=headers,
            params=params,
            body=body,
            retries=retries,
            mode=mode,
        )


