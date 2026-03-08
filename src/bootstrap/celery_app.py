from celery import Celery

from bootstrap.settings import settings

celery_app = Celery(
    "tasks",
    broker=settings.broker_dsn,
    include=[
        "infrastracture.celery_tasks.email_tasks"
    ]
)
