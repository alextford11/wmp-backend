class NotFoundException(Exception):
    def __init__(self, name):
        self.name = name


class IntegrityException(Exception):
    def __init__(self, detail: str):
        self.detail = detail
