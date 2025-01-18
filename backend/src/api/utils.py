from fastapi import Request, Response
from common.data.sqlalchemy.engine import session_maker
from common.data.sqlalchemy.models.api_request import ApiRequest
from datetime import datetime

async def log_to_database(request: Request, response: Response, received_at: datetime, duration_ms: float):
    with session_maker() as session:
        row = ApiRequest()
        row.request_method = request.method
        row.status_code = response.status_code
        row.received_at = received_at.replace(tzinfo=None)
        row.duration_ms = duration_ms
        row.url = str(request.url)
        session.add(row)
        session.commit()
