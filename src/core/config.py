from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8080
    reload: bool = True
    app: str = "main:app_insulin"


class ApiV1PrefixConfig(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"


class ApiPrefixConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1PrefixConfig = ApiV1PrefixConfig()


class DbConfig(BaseModel):
    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = True
    max_overflow: int = 10
    pool_size: int = 30

    naming_convection: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class JwtConfig(BaseModel):
    public: Path = BASE_DIR / "certs" / "jwt-public.pem"
    private: Path = BASE_DIR / "certs" / "jwt-private.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 60 * 24 * 30


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env.dev",
        env_nested_delimiter="__",
        case_sensitive=False,
        env_prefix="APP_CONFIG__",
    )

    db: DbConfig
    run: RunConfig = RunConfig()
    api: ApiPrefixConfig = ApiPrefixConfig()
    jwt: JwtConfig = JwtConfig()


settings: Config = Config()
