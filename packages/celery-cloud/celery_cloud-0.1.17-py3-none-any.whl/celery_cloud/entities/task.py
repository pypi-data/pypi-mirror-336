from typing import Any

from pydantic import BaseModel, Field


class Task(BaseModel):
    """Representation of a celery SQS task

    Args:
        BaseModel (_type_): _description_
    """

    task: str = Field(
        ...,
        max_length=150,
        json_schema_extra={
            "description": "Celery task name",
            "example": "task.add",
        },
    )

    # TODO: should be UUID
    id: str = Field(
        ...,
        max_length=150,
        json_schema_extra={
            "description": "Unique task id",
            "example": "4b8f27d1-cd8b-4b79-a1d5-937c5d3579d7",
        },
    )

    args: list[Any] = Field(
        ...,
        json_schema_extra={
            "description": "Positional arguments for the task",
            "example": "1,2",
        },
    )

    kwargs: dict[str, Any] = Field(
        ...,
        json_schema_extra={
            "description": "Named arguments for the task",
            "example": "{'key': 'value'}",
        },
    )

    retries: int | None = Field(
        default=0,
        json_schema_extra={
            "description": "Number of retries",
            "example": "0",
        },
    )

    eta: str = Field(
        default=None,
        json_schema_extra={
            "description": "Deferred Execution time (ISO8601)",
            "example": "TODO",
        },
    )
