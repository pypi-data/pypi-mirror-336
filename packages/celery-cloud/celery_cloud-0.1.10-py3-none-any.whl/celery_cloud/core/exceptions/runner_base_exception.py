class RunnerBaseException(Exception):
    """Base Domain exception for runner errors

    Args:
        Exception (Exception): inherits from base exception
    """

    def __init__(self, message: str, detail: str | None = None) -> None:
        self.message = message
        self.detail = detail

    def __str__(self) -> str:
        return f"{self.message}: {self.detail}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(message={self.message}, detail={self.detail!r})"
