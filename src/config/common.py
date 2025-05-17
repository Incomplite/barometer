from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
        env_file_encoding="utf-8",
    )
