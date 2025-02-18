from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class DbConfig(BaseModel):
    url: PostgresDsn


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env.dev",
        env_nested_delimiter="__",
        case_sensitive=False,
        env_prefix="APP_CONFIG__",
    )

    db: DbConfig


settings: DbConfig = DbConfig()
