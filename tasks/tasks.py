import asyncio

from celery import Celery

import config
from APINews.db.models.public import News
from APINews.parser.moscow_news_parser import MoscowNewsParser
from utils import constants
from utils.enums import ResponseMode


client = Celery(__name__, broker=config.redis)


@client.task
def parse_news():
    parser = MoscowNewsParser(
        base_url=constants.NEWS_PORTAL_URL, model=News, tag="metro"
    )
    asyncio.get_event_loop().run_until_complete(
        (parser.parse("/news/tags.php?metro", mode=ResponseMode.TEXT.value))
    )
