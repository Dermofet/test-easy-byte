from functools import lru_cache

import pydantic
import pydantic_settings
from dotenv import find_dotenv


class _Settings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_file_encoding="utf-8")


class Settings(_Settings):
    LOG_LEVEL: str = pydantic.Field(..., description="Log level")
    BOT_TOKEN: str = pydantic.Field(..., description="Bot token")
    EXCHANGE_RATE_URL: pydantic.HttpUrl = pydantic.Field(
        ..., description="Exchange rate url"
    )
    EXCHANGE_RATE_API_KEY: str = pydantic.Field(
        ..., description="Exchange rate api key"
    )


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    return Settings(_env_file=find_dotenv(env_file))
