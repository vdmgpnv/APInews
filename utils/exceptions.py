

class BaseError(Exception):
    def __int__(self, message: str = None, original: Exception = None, *args):
        self.message = message
        self.original = original
        super().__init__(message, *args)


class NoDataError(BaseError):
    def __init__(self, message: str = "No data from given url", *args):
        super().__init__(message, *args)