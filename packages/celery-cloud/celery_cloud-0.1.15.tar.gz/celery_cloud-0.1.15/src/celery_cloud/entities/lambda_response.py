from typing import Any

from pydantic import BaseModel, Field


class ProcessedTask(BaseModel):
    """Representation of a successfully processed Celery task"""

    task_id: str = Field(
        ...,
        max_length=150,
        json_schema_extra={
            "description": "Unique ID of the processed task",
            "example": "4b8f27d1-cd8b-4b79-a1d5-937c5d3579d7",
        },
    )

    status: str = Field(
        ...,
        json_schema_extra={
            "description": "Final execution status of the task",
            "example": "SUCCESS",
        },
    )

    result: Any | None = Field(
        default = None,
        json_schema_extra={
            "description": "Returned result of the task if available",
            "example": 15,
        },
    )


class FailedTask(BaseModel):
    """Representation of a failed Celery task"""

    task_id: str | None = Field(
        default = None,
        max_length=150,
        json_schema_extra={
            "description": "Unique ID of the failed task (if extractable)",
            "example": "4b8f27d1-cd8b-4b79-a1d5-937c5d3579d7",
        },
    )

    message_id: str = Field(
        ...,
        json_schema_extra={
            "description": "Unique identifier of the SQS message that failed",
            "example": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
        },
    )

    error: str = Field(
        ...,
        json_schema_extra={
            "description": "Error message explaining why the task failed",
            "example": "JSONDecodeError: Invalid JSON format",
        },
    )


class LambdaResponse(BaseModel):
    """Unified response model for AWS Lambda processing Celery tasks"""

    status: str = Field(
        ...,
        json_schema_extra={
            "description": "Overall execution status of the batch processing",
            "example": "completed",
        },
    )

    processed_messages: int | None = Field(
        default = None,
        json_schema_extra={
            "description": "Total number of messages successfully processed",
            "example": 5,
        },
    )

    failed_messages: int | None = Field(
        default = None,
        json_schema_extra={
            "description": "Total number of messages that failed processing",
            "example": 2,
        },
    )

    processed_tasks: list[ProcessedTask] | None = Field(
        default = None,
        json_schema_extra={
            "description": "List of successfully processed tasks",
        },
    )

    failed_tasks: list[FailedTask] | None = Field(
        default = None,
        json_schema_extra={
            "description": "List of failed tasks with details",
        },
    )

    message: str | None = Field(
        default = None,
        json_schema_extra={
            "description": ("Error message if the entire Lambda execution failed"),
            "example": "Invalid SQS event format",
        },
    )

    details: str | None = Field(
        default = None,
        json_schema_extra={
            "description": "Detailed error information if applicable",
            "example": (
                '{"loc": ["Records"], "msg": "field required", '
                '"type": "value_error.missing"}'
            ),
        },
    )
