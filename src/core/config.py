from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8080
    reload: bool = True
    app: str = "main:app_insulin"


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
    run: RunConfig = RunConfig()


settings: Config = Config()
