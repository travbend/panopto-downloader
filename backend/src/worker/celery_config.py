from common.config import settings
from kombu import Queue

broker_url = settings.celery_broker_url
result_backend = settings.celery_backend_url
worker_prefetch_multiplier = 1
worker_concurrency = settings.worker_concurrency
result_expires = settings.worker_result_expiry_seconds

task_default_queue = 'default'
task_default_priority = 1
task_queues = [
    Queue('default', routing_key='default',
          queue_arguments={'x-max-priority': 10}),
]