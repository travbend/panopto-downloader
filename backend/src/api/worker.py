from celery import Celery
from celery.result import AsyncResult
from uuid import UUID
from common.config import settings

worker = Celery('worker', broker=settings.celery_broker_url, backend=settings.celery_backend_url)

def get_result(task_id: UUID):
    return AsyncResult(str(task_id), app=worker)