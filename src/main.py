import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_offline import FastAPIOffline

from src.api.routers import get_apps_router
from src.config import app_config, project_config

app: FastAPI = FastAPIOffline(**app_config)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)


app.include_router(get_apps_router())


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=project_config.APP_HOST,
        port=int(project_config.APP_PORT),
        reload=project_config.RELOAD,
        use_colors=True,
    )
