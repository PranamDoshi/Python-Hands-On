"""Configuration settings for the application."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # Database settings
    SQL_DATABASE_URL: str = "postgresql://user:password@localhost:5432/crawl_db"
    MONGODB_URL: str = "mongodb://localhost:27017/"
    MONGODB_DB_NAME: str = "crawl_data"
    
    # Queue settings
    REDIS_URL: str = "redis://localhost:6379/0"
    EXTRACTOR_QUEUE_NAME: str = "extractor_queue"
    CRAWLER_QUEUE_NAME: str = "crawler_queue"
    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Airflow settings
    AIRFLOW_HOME: str = "/opt/airflow"
    
    # Scheduler settings
    SCHEDULER_INTERVAL_SECONDS: int = 60
    PDP_SCHEDULER_INTERVAL_SECONDS: int = 30
    
    # Worker settings
    EXTRACTOR_WORKER_POLL_INTERVAL: int = 5
    CRAWLER_WORKER_POLL_INTERVAL: int = 5
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
