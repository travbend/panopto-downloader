from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List

class Settings(BaseSettings):
    project_name: str = "panopto-downloader"
    api_url_prefix: str = "/api/v1"

    debug_api: bool = False
    debug_worker: bool = False
    debug_wait: bool = False
    
    ffmpeg_timeout_seconds: int = 60
    result_cleanup_delay_seconds: int = 300
    result_cleanup_cycle_seconds: int = 60
    
    worker_concurrency: int = 4
    worker_result_expiry_seconds: int = 300
    
    postgres_db: Optional[str] = None
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None
    
    rabbitmq_user: Optional[str] = None
    rabbitmq_password: Optional[str] = None

    redis_db: Optional[int] = 0
    redis_password: Optional[str] = None
    
    b2_token_seconds: int = 300
    b2_bucket_name: Optional[str] = None
    b2_application_key_id: Optional[str] = None
    b2_application_key: Optional[str] = None
    
    shared_files_path: Optional[str] = None
    
    @property
    def sqlalchemy_connection_string(self) -> str:
        return f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}@postgres:5432/{self.postgres_db}"
    
    @property
    def celery_broker_url(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@rabbitmq:5672//"
    
    @property
    def celery_backend_url(self) -> str:
        return f"redis://:{self.redis_password}@redis:6379/{self.redis_db}"
    
    model_config = SettingsConfigDict(
        secrets_dir='/run/secrets'
    )
    
settings = Settings()