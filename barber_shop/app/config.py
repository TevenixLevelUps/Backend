from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class DatabaseConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str

class RedisConfig(BaseModel):
    host: str
    port: int
    cache_expire_seconds: int
    rate_limit_per_minute: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    db: DatabaseConfig
    redis: RedisConfig


settings = Settings()