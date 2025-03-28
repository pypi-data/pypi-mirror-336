from typing import Any

from pydantic import BaseModel, Field


class TaskResult(BaseModel):
    """Model for the result of a task

    Args:
        BaseModel (_type_): _description_
    """

    status: str = Field(
        ...,
        json_schema_extra={"description": "Task Status", "example": "SUCCESS"},
    )

    result: Any | None = Field(
        default = None,
        json_schema_extra={"description": "Task result", "example": 5},
    )

    traceback: str | None = Field(
        default = None,
        json_schema_extra={
            "description": "Error traceback if the task failed",
            "example": None,
        },
    )

    children: list[Any] = Field(
        default_factory=list,
        json_schema_extra={
            "description": "List of children tasks",
            "example": [],
        },
    )

    date_done: str | None = Field(
        default = None,
        json_schema_extra={
            "description": "Finish data format ISO 8601",
            "example": "2025-03-11T09:56:48.043888+00:00",
        },
    )

    task_id: str = Field(
        ...,
        json_schema_extra={
            "description": "Unique task ID",
            "example": "84e50a89-92f9-4b97-95b5-eb4bad279205",
        },
    )
