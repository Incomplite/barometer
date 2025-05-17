from src.config.auth import AuthConfig
from src.config.common import CommonSettings
from src.config.db import DatabaseConfig


class ProjectConfig(CommonSettings):
    DEBUG: bool
    RELOAD: bool
    DB_ECHO_LOG: bool
    PROJECT_TITLE: str
    APP_HOST: str
    APP_PORT: str | int

    auth: AuthConfig = AuthConfig()  # type: ignore
    db: DatabaseConfig = DatabaseConfig()  # type: ignore


project_config = ProjectConfig()  # type: ignore


def get_app_settings(project_config: ProjectConfig) -> dict:
    app_config = {
        "title": project_config.PROJECT_TITLE,
        "debug": project_config.DEBUG,
    }

    if not project_config.DEBUG:
        app_config["openapi_url"] = None

    return app_config


app_config = get_app_settings(project_config)
