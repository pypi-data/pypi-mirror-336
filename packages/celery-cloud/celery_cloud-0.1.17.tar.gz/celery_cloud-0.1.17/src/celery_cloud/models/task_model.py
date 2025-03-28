import base64
import json
from datetime import UTC, datetime
from typing import Any

from pynamodb.attributes import (
    BinaryAttribute,
    NumberAttribute,
    UnicodeAttribute,
)
from pynamodb.models import Model

from celery_cloud.entities import TaskResult
from celery_cloud.exceptions import BackendException
from celery_cloud.logging import logger
from celery_cloud.settings import settings


class TaskModel(Model):
    """Dynamodb model to store Celery tasks.

    Args:
        Model (_type_): _description_

    Returns:
        _type_: _description_
    """

    class Meta:
        table_name = settings.CELERY_BACKEND_TABLE
        region = settings.CELERY_BACKEND_REGION

    # task_id has b'celery-task-meta-' prefix before UUID
    id = UnicodeAttribute(hash_key=True)

    # Result stored as binary (base64)
    result = BinaryAttribute(legacy_encoding=False)

    # Timestamp as floating number
    timestamp = NumberAttribute(default=lambda: datetime.now(UTC).timestamp())

    @classmethod
    def insert_task(cls, task_uuid: str) -> "TaskModel":
        """Insert a new task with the correct prefix.

        Args:
            task_uuid (str): _description_

        Returns:
            _type_: _description_
        """

        try:
            logger.debug(f"Inserting task {task_uuid}")

            prefixed_task_id = f"celery-task-meta-{task_uuid}".encode()

            task_result = TaskResult(
                status="PROCESSING",
                result=None,
                traceback=None,
                children=[],
                date_done=str(datetime.now(UTC).isoformat()),
                task_id=task_uuid,
            )

            encoded_result = json.dumps(task_result.model_dump()).encode()

            task = cls(id=str(prefixed_task_id), result=encoded_result)
            task.save()

            logger.debug(f"Task {task_uuid} inserted on DynamoDB")

            return task

        except Exception as e:
            logger.error(f"Error inserting task {task_uuid}: {str(e)}")
            raise BackendException(
                message=f"Error inserting task {task_uuid}: {str(e)}",
                detail=str(e),
            ) from e

    @classmethod
    def update_task(
        cls,
        task_uuid: str,
        status: str,
        result: Any | None = None,
        traceback: str | None = None,
    ):
        """Update task status

        Args:
            task_uuid (str): _description_
            status (str): _description_
            result (Optional[Any], optional): Defaults to None.
            traceback (Optional[str], optional): Defaults to None.

        Returns:
            _type_: _description_
        """

        logger.debug(f"Updating task {task_uuid} with status {status}")

        prefixed_task_id = f"celery-task-meta-{task_uuid}".encode()

        try:
            task = cls.get(str(prefixed_task_id))

            task_result = TaskResult(
                status=status,
                result=result,
                traceback=traceback if traceback else None,
                children=[],
                date_done=str(datetime.now(UTC).isoformat()),
                task_id=task_uuid,
            )

            encoded_result = json.dumps(task_result.model_dump()).encode()

            task.update(
                actions=[
                    cls.result.set(encoded_result),
                    cls.timestamp.set(datetime.now(UTC).timestamp()),
                ]
            )

            logger.debug(f"Task {task_uuid} updated on DynamoDB")

            return task
        except cls.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error updating task {task_uuid}: {str(e)}")
            raise BackendException(
                message=f"Error updating task {task_uuid}: {str(e)}",
                detail=str(e),
            ) from e

    @classmethod
    def get_task(cls, task_uuid: str) -> dict | None:
        """Ges task status and decode result

        Args:
            task_uuid (str): _description_

        Returns:
            Optional[dict]: _description_
        """

        logger.debug(f"Getting task {task_uuid}")

        prefixed_task_id = f"celery-task-meta-{task_uuid}".encode()

        try:
            task = cls.get(str(prefixed_task_id))

            decoded_result = (
                json.loads(base64.b64decode(task.result).decode())
                if task.result
                else None
            )

            logger.debug(f"Task {task_uuid} retrieved from DynamoDB")

            return {
                "task_id": str(prefixed_task_id),  # task.task_id,
                "result": decoded_result,
                "timestamp": task.timestamp,
            }
        except cls.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting task {task_uuid}: {str(e)}")
            raise BackendException(
                message=f"Error getting task {task_uuid}: {str(e)}",
                detail=str(e),
            ) from e
