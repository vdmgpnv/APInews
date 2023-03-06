from parser.request_client import RequestClient


class Parser:

    def __init__(self, client: RequestClient):
        self.client = client
