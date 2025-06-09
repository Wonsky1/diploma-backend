"""Define configuration settings using Pydantic and manage environment variables."""

from enum import StrEnum
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class JobStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Exchanges(StrEnum):
    ROBOT_COMMAND = "robot_command"


class Queues(StrEnum):
    PENDING = "pending"

class Settings(BaseSettings):
    """Class defining configuration settings using Pydantic."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    RABBITMQ_URL: str
    RABBITMQ_EXCHANGES: List[Exchanges] = [
        Exchanges.ROBOT_COMMAND,
    ]
    RABBITMQ_QUEUES: List[Queues] = [Queues.PENDING]

    API_VERSION: str = "0.1.0"


settings = Settings()
