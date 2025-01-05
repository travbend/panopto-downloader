from worker.main import app
from celery.result import AsyncResult
from uuid import UUID

def get_result(task_id: UUID):
    return AsyncResult(str(task_id), app=app)