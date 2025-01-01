from fastapi import FastAPI
from config import settings
from startup import initialize

app: FastAPI = None

if app == None:
    if settings.debug_api:
        import debugpy # type: ignore
        debugpy.listen(("0.0.0.0", 5678))
        if settings.debug_wait:
            debugpy.wait_for_client()

    root_path = settings.project_name + settings.api_url_prefix
    app = FastAPI(root_path=root_path)

    initialize(app)