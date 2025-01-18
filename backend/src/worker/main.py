from celery import Celery
from celery.signals import worker_init
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

initialize()