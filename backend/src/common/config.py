from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List

class Settings(BaseSettings):
    project_name: str = "panopto-downloader"
    api_url_prefix: str = "/api/v1"

    debug_api: bool = False
    debug_worker: bool = False
    debug_wait: bool = False

    sqlalchemy_connection_string: Optional[str] = None
    celery_broker_url: Optional[str] = None
    celery_backend_url: Optional[str] = None
    shared_files_path: Optional[str] = None
    
settings = Settings()