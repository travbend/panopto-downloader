from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from common.config import settings
from api.startup import initialize
from api.utils import log_to_database
import time
import asyncio
from datetime import datetime, timezone

if settings.debug_api:
    import debugpy # type: ignore
    debugpy.listen(("0.0.0.0", 5678))
    if settings.debug_wait:
        debugpy.wait_for_client()

root_path = settings.project_name + settings.api_url_prefix
app = FastAPI(root_path=root_path)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.hosted\.panopto\.com",
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    received_at = datetime.now(timezone.utc)
    response = await call_next(request)
    process_time = (datetime.now(timezone.utc) - received_at).total_seconds() * 1000
    asyncio.create_task(log_to_database(request, response, received_at, process_time))
    return response

initialize(app)