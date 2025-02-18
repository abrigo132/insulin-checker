from pydantic_settings import BaseSettings
from pydantic import BaseModel, PostgresDsn
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class DbConfig(BaseModel):
    url: PostgresDsn
