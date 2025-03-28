import contextvars
import sys

from loguru import logger

from .settings import settings

# Create a context variable to store the trace_id
trace_id_context = contextvars.ContextVar("trace_id", default=None)


def add_trace_id(record) -> bool:
    """Add the trace_id to the log record

    Args:
        record (_type_): _description_
    """
    trace_id = trace_id_context.get()
    record["extra"]["trace_id"] = trace_id if trace_id else "N/A"
    return True  # Return True to indicate the filter passed


# Configure the logger
logger.remove()

# stderr Logger
logger.add(
    sink=sys.stderr,
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    filter=add_trace_id,
    colorize=True,
    serialize=False,
    backtrace=True,
    diagnose=True,
    enqueue=settings.LOG_ENQUEUE,  # Do not uses multiprocesing for the logs (aws lambda)
)

__all__ = [
    "logger",
    "trace_id_context",
]  # Add  to __all__ to be able to import them from the package
