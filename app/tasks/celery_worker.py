from celery import Celery
from app.config import settings

celery_app = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
)

@celery_app.task
def example_task():
    return "Hello from Celery!"