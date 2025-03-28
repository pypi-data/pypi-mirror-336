import base64
import json
from typing import Any

from pydantic import BaseModel, Field


class DeliveryInfo(BaseModel):
    """Delivery information for the SQS message."""

    exchange: str = Field(
        ...,
        json_schema_extra={"description": "Exchange used for message delivery."},
    )
    routing_key: str = Field(
        ..., json_schema_extra={"description": "Routing key used in SQS."}
    )


class Properties(BaseModel):
    """Properties of the SQS message."""

    correlation_id: str = Field(
        ..., json_schema_extra={"description": "Correlation ID for the task."}
    )
    reply_to: str = Field(
        ..., json_schema_extra={"description": "Reply queue identifier."}
    )
    delivery_mode: int = Field(
        ...,
        json_schema_extra={"description": "Delivery mode (2 for persistent messages)."},
    )
    delivery_info: DeliveryInfo = Field(
        ..., json_schema_extra={"description": "Message delivery details."}
    )
    priority: int = Field(
        ...,
        json_schema_extra={"description": "Priority level of the message."},
    )
    body_encoding: str = Field(
        ...,
        json_schema_extra={
            "description": "Encoding format of the message body (base64)."
        },
    )
    delivery_tag: str = Field(
        ...,
        json_schema_extra={"description": "Unique delivery tag for the message."},
    )


class Headers(BaseModel):
    """Metadata headers for the Celery task."""

    lang: str = Field(
        ...,
        json_schema_extra={"description": "Programming language used (e.g., 'py')."},
    )
    task: str = Field(..., json_schema_extra={"description": "Celery task path."})
    id: str = Field(..., json_schema_extra={"description": "Unique task ID."})
    shadow: str | None = Field(
        None, json_schema_extra={"description": "Task shadow, if applicable."}
    )
    eta: str | None = Field(
        None, json_schema_extra={"description": "Estimated time of execution."}
    )
    expires: str | None = Field(
        None, json_schema_extra={"description": "Expiration date of the task."}
    )
    group: str | None = Field(
        None,
        json_schema_extra={"description": "Celery task group identifier."},
    )
    group_index: int | None = Field(
        None, json_schema_extra={"description": "Group index if applicable."}
    )
    retries: int = Field(
        ..., json_schema_extra={"description": "Number of retries attempted."}
    )
    timelimit: list[int | None] = Field(
        ..., json_schema_extra={"description": "Execution time limits."}
    )
    root_id: str = Field(..., json_schema_extra={"description": "Root task ID."})
    parent_id: str | None = Field(
        None, json_schema_extra={"description": "Parent task ID, if any."}
    )
    argsrepr: str = Field(
        ...,
        json_schema_extra={
            "description": "String representation of positional arguments."
        },
    )
    kwargsrepr: str = Field(
        ...,
        json_schema_extra={
            "description": "String representation of keyword arguments."
        },
    )
    origin: str = Field(
        ..., json_schema_extra={"description": "Task origin (hostname)."}
    )
    ignore_result: bool = Field(
        ...,
        json_schema_extra={
            "description": "Indicates whether the result should be ignored."
        },
    )
    replaced_task_nesting: int = Field(
        ...,
        json_schema_extra={"description": "Nesting level of replaced tasks."},
    )
    stamped_headers: Any | None = Field(
        None,
        json_schema_extra={"description": "Stamped headers if available."},
    )
    stamps: dict[str, Any] = Field(
        ...,
        json_schema_extra={"description": "Additional metadata about the task."},
    )


class SQSMessage(BaseModel):
    """Model representing an SQS message containing a Celery task."""

    body: str = Field(
        ..., json_schema_extra={"description": "Base64-encoded message body."}
    )
    content_encoding: str = Field(
        ...,
        json_schema_extra={"description": "Content encoding type (utf-8)."},
    )
    content_type: str = Field(
        ...,
        json_schema_extra={
            "description": "MIME type of the content (application/json)."
        },
    )
    headers: Headers = Field(
        ..., json_schema_extra={"description": "Celery task metadata headers."}
    )
    properties: Properties = Field(
        ..., json_schema_extra={"description": "Message properties from SQS."}
    )

    def decode_body(self) -> Any:
        """Decodes the base64-encoded message body into a Python object."""
        decoded_json = base64.b64decode(self.body).decode("utf-8")
        return json.loads(decoded_json)


class SQSAttributes(BaseModel):
    """Metadata attributes of the SQS message."""

    ApproximateReceiveCount: str = Field(
        ...,
        json_schema_extra={
            "description": (
                "Number of times the message has been received but not deleted."
            )
        },
    )
    SentTimestamp: str = Field(
        ...,
        json_schema_extra={
            "description": (
                "Timestamp when the message was sent (milliseconds since epoch)."
            )
        },
    )
    ApproximateFirstReceiveTimestamp: str = Field(
        ...,
        json_schema_extra={
            "description": (
                "Timestamp when the message was first received "
                "(milliseconds since epoch)."
            )
        },
    )


class SQSRecord(BaseModel):
    """Model representing a single SQS message."""

    messageId: str = Field(
        ...,
        json_schema_extra={"description": "Unique identifier for the message."},
    )
    receiptHandle: str = Field(
        ...,
        json_schema_extra={
            "description": (
                "Receipt handle used for deleting or modifying the message."
            )
        },
    )
    body: str = Field(
        ...,
        json_schema_extra={
            "description": "Base64-encoded message body containing task data."
        },
    )
    attributes: SQSAttributes = Field(
        ...,
        json_schema_extra={"description": "Metadata attributes of the SQS message."},
    )
    eventSource: str = Field(
        ...,
        json_schema_extra={"description": "Source of the event (e.g., 'aws:sqs')."},
    )
    eventSourceARN: str = Field(
        ..., json_schema_extra={"description": "ARN of the SQS queue."}
    )

    def get_message(self) -> Any:
        """Decodes the base64-encoded body into a JSON dictionary."""
        return json.loads(base64.b64decode(self.body).decode("utf-8"))


class SQSEvent(BaseModel):
    """Representation of an AWS SQS event.

    Args:
        BaseModel (_type_): Pydantic base model.
    """

    Records: list[SQSRecord] = Field(
        ...,
        json_schema_extra={
            "description": "List of messages received in the SQS event.",
        },
    )
