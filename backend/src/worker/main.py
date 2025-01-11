from celery import Celery
from celery.signals import worker_init
from kombu import Exchange, Queue
from common.config import settings
from worker.startup import initialize

@worker_init.connect
def on_worker_init(sender=None, **kwargs):
    if settings.debug_worker:
        import debugpy # type: ignore
        debugpy.listen(("0.0.0.0", 5679))
        if settings.debug_wait:
            debugpy.wait_for_client()

app = Celery('worker')
app.config_from_object('worker.celery_config')

app.conf.task_default_queue = 'default'
app.conf.task_default_priority = 1
app.conf.task_queues = [
    Queue('default', routing_key='default',
          queue_arguments={'x-max-priority': 10}),
]

initialize()