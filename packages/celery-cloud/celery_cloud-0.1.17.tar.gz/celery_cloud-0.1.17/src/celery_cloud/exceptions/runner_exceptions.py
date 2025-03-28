from .runner_base_exception import (
    RunnerBaseException,
)


class BackendException(RunnerBaseException):
    """Domain exception for backend errors"""

    ...


class EventDecodeException(RunnerBaseException):
    """Domain exception for message decoding errors"""

    ...


class MessageDecodeException(RunnerBaseException):
    """Domain exception for message decoding errors"""

    ...


class TaskDecodeException(RunnerBaseException):
    """Domain exception for task decoding errors"""

    ...


class TaskExecutionException(RunnerBaseException):
    """Domain exception for execution exceptions"""

    ...
