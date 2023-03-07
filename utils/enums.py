from enum import Enum


class ResponseMode(Enum):
    JSON = "json"
    TEXT = "text"
    COOKIES = "cookies"
    HEADERS = "headers"
    BINARY = "binary"

