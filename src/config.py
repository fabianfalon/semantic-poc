from typing import Optional

from pydantic import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    """Common application settings."""

    app_title: str = "Embeddings API with DDD + OpenAI + LangChain"
    app_name: str = "fastapi"
    debug: bool = False
    swagger_url: str = "/docs"
    model_config = SettingsConfigDict(extra="allow")


class ServerSettings(BaseSettings):
    """
    Gunicorn server settings
    """

    host: str = "127.0.0.1"
    port: int = 5000
    workers_per_core: int = 1
    max_workers: Optional[int] = None
    log_level: str = "info"
    graceful_timeout: int = 120
    timeout: int = 120
    keep_alive: int = 5
    model_config = SettingsConfigDict(extra="allow")


class Settings(CommonSettings, ServerSettings):
    """Main settings class that aggregates all configurations."""

    debug: bool = False
    open_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


settings = Settings()
