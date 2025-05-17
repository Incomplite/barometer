from pydantic_settings import SettingsConfigDict

from src.config.common import CommonSettings


class AuthConfig(CommonSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    INITIAL_ADMIN_USERNAME: str
    INITIAL_ADMIN_PASSWORD: str

    model_config = SettingsConfigDict(env_prefix="AUTH_")
