import ast
import json
from typing import Any, NamedTuple
from urllib.parse import parse_qs, urlparse

import boto3
from ksuid import Ksuid
from pydantic import ValidationError

from celery_cloud.entities import (
    Task,
    FailedTask,
    LambdaResponse,
    ProcessedTask,
    SQSEvent,
    SQSMessage,
    SQSRecord,
)
from celery_cloud.exceptions import (
    BackendException,
    EventDecodeException,
    MessageDecodeException,
    TaskDecodeException,
    TaskExecutionException,
)
from celery_cloud.logging import logger, trace_id_context
from celery_cloud.models.task_model import TaskModel
from celery_cloud.settings import settings


class TaskRoute(NamedTuple):
    scheme: str  # task / lambda / etc.
    module: str  # module or lambda arn (as host)
    function: str  # function path or callable name
    query: dict  # parsed query params if any


def parse_task_url(url: str) -> TaskRoute:
    parsed = urlparse(url)

    scheme = parsed.scheme  # 'task' or 'lambda'
    module = parsed.netloc  # module path or ARN
    function = parsed.path.lstrip("/")  # remove leading slash
    query = parse_qs(parsed.query)

    return TaskRoute(scheme, module, function, query)


def call_lambda_task(task: Task, route: TaskRoute) -> Any:
    """Execute a task defined in a remote lambda function

    Args:
        task (Task): Task to execute

    Returns:
        Any: Task execution result

    """

    logger.debug(f"Calling lambda task: {route.module}")

    region = route.module.split(":")[3]
    logger.debug(f"Lambda function on region: {region}")

    # Build the lambda client
    lambda_client = boto3.client("lambda", region_name=region)

    # Execute the lambda function
    response = lambda_client.invoke(
        FunctionName=route.module,
        InvocationType="RequestResponse",
        Payload=json.dumps(
            {
                "args": task.args,
                "kwargs": task.kwargs,
            }
        ),
    )

    logger.debug(f"Raw response: {response}")

    # Parse the response
    response_payload = json.loads(response["Payload"].read())

    logger.debug(f"Response payload: {response_payload}")

    # Check if the lambda function returned an error
    if "FunctionError" in response:
        raise TaskExecutionException(
            message=f"Lambda function {route.module} returned an error",
            detail=response_payload,
        )

    return response_payload["body"] if "body" in response_payload else response_payload


def call_local_task(task: Task, route: TaskRoute) -> Any:
    """Execute a task defined in the local application

    Args:
        task (Task): Celery task to execute

    Returns:
        Any: Task execution result

    """

    logger.debug(f"Calling local task: {route.module}.{route.function}")

    # Import module
    module = __import__(route.module, fromlist=[route.function])
    function = getattr(module, route.function)

    # Execute function
    task_result = function(task.args, task.kwargs)

    return task_result


def call_task(task: Task) -> Any:
    """Execute a Celery task and return the result

    Args:
        task (Task): Celery task to execute

    Returns:
        Any: Task execution result

    """

    # TODO: allow to call remote lambda functions

    try:
        # Get task configuration
        task_config = settings.TASKS[task.task]
        route = parse_task_url(task_config)

        if route.scheme == "lambda":
            task_result = call_lambda_task(task, route)
        elif route.scheme == "task":
            task_result: Any = call_local_task(task, route)
        else:
            raise TaskExecutionException(
                message=f"Unsupported task scheme: {route.scheme}",
                detail=route.scheme,
            )

        logger.debug(f"Executed task: {task.task} with ID {task.id}")

        return task_result

    except Exception as e:
        logger.error(f"Exception executing task {task.id}: {str(e)}")

        raise TaskExecutionException(
            message=f"Exception executing task {task.id}", detail=str(e)
        ) from e


def get_event(event: dict[str, Any]) -> SQSEvent:
    """Get SQSEvent from message

    Args:
        event (dict[str, Any]): SQS event

    Returns:
        SQSEVent: Decoded event
    """

    try:
        # Validate the event with Pydantic
        sqs_event: SQSEvent = SQSEvent(**event)
        return sqs_event
    except ValidationError as e:
        logger.error(f"Invalid SQS event format: {e.json()}")
        raise EventDecodeException(
            message="Invalid SQS event format", detail=e.json()
        ) from e
    except Exception as e:
        logger.error(f"Error decoding event: {str(e)}")
        raise EventDecodeException(message="Error decoding event", detail=str(e)) from e


def get_message(record: SQSRecord) -> SQSMessage:
    """Get message from SQS record

    Args:
        record (SQSRecord): _description_

    Returns:
        SQSMessage: _description_
    """

    # 3.1. Get Message from record
    try:
        message: dict[str, Any] = record.get_message()
        # TODO: validate fields exist
        sqs_message: SQSMessage = SQSMessage(
            body=message["body"],
            content_encoding=message["content-encoding"],
            content_type=message["content-type"],
            headers=message["headers"],
            properties=message["properties"],
        )

        return sqs_message

    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError processing message: {str(e)}")

        raise MessageDecodeException(
            message="JSONDecodeError processing message", detail=str(e)
        ) from e

    except ValidationError as e:
        logger.error(f"ValidationError processing message: {str(e)}")
        raise MessageDecodeException(
            message="ValidationError processing message", detail=str(e)
        ) from e

    except Exception as e:
        logger.error(f"Exception processing message: {str(e)}")

        raise MessageDecodeException(
            message="Exception processing message", detail=str(e)
        ) from e


def get_task(message: SQSMessage) -> Task:
    """Get Task from message

    Args:
        message (SQSMessage): _description_

    Returns:
        Task: _description_
    """

    # 3.1. Get Message from record
    try:
        # Create Task object
        task: Task = Task(
            id=message.headers.id,
            task=message.headers.task,
            args=ast.literal_eval(
                message.headers.argsrepr
            ),  # Safely convert string to list
            kwargs=ast.literal_eval(
                message.headers.kwargsrepr
            ),  # Safely convert string to dict
        )

        return task

    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError getting task: {str(e)}")

        raise TaskDecodeException(
            message="JSONDecodeError getting task", detail=str(e)
        ) from e

    except ValidationError as e:
        logger.error(f"ValidationError getting task: {str(e)}")
        raise TaskDecodeException(
            message="ValidationError getting task", detail=str(e)
        ) from e

    except Exception as e:
        logger.error(f"Exception getting task: {str(e)}")

        raise TaskDecodeException(
            message="Exception getting task", detail=str(e)
        ) from e


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Lambda handler for processing Celery Broker events

    Args:
        event (dict[str, Any]): _description_
        context (Any): _description_

    Returns:
        dict[str, Any]: _description_
    """

    # TODO: refactor this function to make it more readable

    processed_tasks: list[ProcessedTask] = []
    failed_tasks: list[FailedTask] = []

    # Logging: Generate KSUID as trace_id
    trace_id = str(Ksuid())
    # Logging: Assign trace_id to context
    trace_id_context.set(trace_id)

    logger.debug(f"Processing lambda event: {event} with context: {context}")

    logger.debug(f"Settings TASKS: {settings.TASKS}")

    try:
        # 1. Decode the event depending on the event source
        # TODO: Only SQS managed by now, add more event types

        sqs_event: SQSEvent = get_event(event)

        logger.debug(f"Processing lambda event: {sqs_event.model_dump()}")

        # 3. Process the event
        for record in sqs_event.Records:
            message: dict[str, Any] = record.get_message()
            # TODO: validate fields exist
            sqs_message: SQSMessage = SQSMessage(
                body=message["body"],
                content_encoding=message["content-encoding"],
                content_type=message["content-type"],
                headers=message["headers"],
                properties=message["properties"],
            )
            logger.debug(f"Processing message: {sqs_message}")

            # 3.2. Get celery Task from message
            task: Task = get_task(sqs_message)
            logger.debug(f"Processing task: {task}")

            # Set task status to "PROCESSING" in backend
            TaskModel.insert_task(task_uuid=task.id)

            # 3.3. Check if task is supported
            if task.task not in settings.TASKS:
                logger.error(f"Task '{task.task}' not supported")

                failed_tasks.append(
                    FailedTask(
                        message_id=record.messageId,
                        task_id=task.id,
                        error=f"Task '{task.task}' not supported",
                    )
                )

                # 3.3.1. Update task status and result in backend
                TaskModel.update_task(task.id, status="ERROR", result=None)

                continue

            # 3.4. Call function with args and kwargs
            task_result: Any = call_task(task)

            logger.debug(f"Processed task: {task.task} with ID {task.id}")

            # 3.5. Update task status and result in backend
            TaskModel.update_task(
                task.id, status="SUCCESS", result=task_result
            )

            # 3.6. Append task to processed tasks
            processed_tasks.append(
                ProcessedTask(
                    task_id=task.id,
                    status="SUCCESS",
                    result=task_result,
                )
            )

        # Clear context before finishing the function
        trace_id_context.set(None)

        return LambdaResponse(
            status="completed",
            processed_messages=len(processed_tasks),
            failed_messages=len(failed_tasks),
            processed_tasks=processed_tasks if processed_tasks else None,
            failed_tasks=failed_tasks if failed_tasks else None,
        ).model_dump()

    except (
        MessageDecodeException,
        TaskDecodeException,
        BackendException,
        TaskExecutionException,
    ) as e:
        failed_tasks.append(
            FailedTask(
                message_id=record.messageId,
                error=f"{str(e)}",
            )
        )

    # TODO: Add more specific error handling (Exception) to capture all errors
    except EventDecodeException as e:
        # Clear context before finishing the function
        trace_id_context.set(None)

        return LambdaResponse(
            status="error",
            message=e.message,
            details=e.detail,
        ).model_dump()

    except Exception as e:
        # Clear context before finishing the function
        trace_id_context.set(None)

        return LambdaResponse(
            status="error",
            message=f"General error: {str(e)}",
            details=str(e),
        ).model_dump()
