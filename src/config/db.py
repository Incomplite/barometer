from pydantic import PostgresDsn
from pydantic_settings import SettingsConfigDict

from src.config.common import CommonSettings


class DatabaseConfig(CommonSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB_NAME: str

    model_config = SettingsConfigDict(env_prefix="DB_")

    @property
    def database_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB_NAME,
        )
