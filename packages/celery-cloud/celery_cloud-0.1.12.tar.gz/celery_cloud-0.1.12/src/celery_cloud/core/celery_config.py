from celery_cloud.core.settings import settings


class Celeryconfig:
    # imports: tuple = ("celery_app.tasks",)
    broker_connection_retry_on_startup: bool = True
    task_create_missing_queues: bool = True
    worker_enable_remote_control: bool = False
    worker_send_task_events: bool = False

    def __init__(self):
        self.task_default_queue = settings.CELERY_TASK_DEFAULT_QUEUE

        self.broker_url = settings.CELERY_BROKER_URL
        self.result_backend = settings.CELERY_BACKEND_URL

        if self.broker_url.startswith("sqs"):
            self.broker_transport_options = {
                "predefined_queues": {
                    f"{settings.CELERY_TASK_DEFAULT_QUEUE}": {
                        "url": settings.CELERY_BROKER_SQS_QUEUE_URL,
                    },
                },
                "region": settings.CELERY_BROKER_SQS_REGION,
                "visibility_timeout": 3600,  # 1 hour
                "polling_interval": 10,
                # "queue_name_prefix": settings.CELERY_TASK_DEFAULT_QUEUE,
                "dead_letter_queue": (
                    f"{settings.CELERY_TASK_DEFAULT_QUEUE}-dlq",
                ),
            }
