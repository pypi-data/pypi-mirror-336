from celery_cloud.core.exceptions.runner_base_exception import (
    RunnerBaseException,
)


class BackendException(RunnerBaseException):
    """Domain exception for backend errors"""

    ...


class EventDecodeException(Exception):
    """Domain exception for message decoding errors"""

    ...


class MessageDecodeException(Exception):
    """Domain exception for message decoding errors"""

    ...


class TaskDecodeException(Exception):
    """Domain exception for task decoding errors"""

    ...


class TaskExecutionException(Exception):
    """Domain exception for execution exceptions"""

    ...
