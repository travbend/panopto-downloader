from celery import Celery
from celery.result import AsyncResult
from uuid import UUID
from common.config import settings
from kombu import Queue

worker = Celery('worker', broker=settings.celery_broker_url, backend=settings.celery_backend_url)
worker.conf.task_default_queue = 'default'
worker.conf.task_default_priority = 1
worker.conf.task_queues = [
    Queue('default', routing_key='default',
          queue_arguments={'x-max-priority': 10}),
]

def get_result(task_id: UUID):
    return AsyncResult(str(task_id), app=worker)