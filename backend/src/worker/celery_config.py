from common.config import settings

broker_url = settings.celery_broker_url
result_backend = settings.celery_backend_url
worker_prefetch_multiplier = 1
worker_concurrency = settings.worker_concurrency