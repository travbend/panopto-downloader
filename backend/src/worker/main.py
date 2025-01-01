from celery import Celery
from config import settings
from startup import initialize

if settings.debug_worker:
    import debugpy # type: ignore
    debugpy.listen(("0.0.0.0", 5679))
    if settings.debug_wait:
        debugpy.wait_for_client()

app = Celery('worker')
app.config_from_object('celery_config')

initialize()