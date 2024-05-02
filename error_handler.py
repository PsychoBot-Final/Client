class ADBError(Exception):
    def __init__(self, message: str, code: int) -> None:
        super().__init__(message)
        self.code = code