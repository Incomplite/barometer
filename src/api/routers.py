from fastapi import APIRouter

from src.auth.controllers import auth_router
from src.entities.bar.controllers import bar_router
from src.entities.cocktail.controllers import cocktail_router
from src.entities.tag.controllers import tag_router
from src.entities.user.controllers import user_router


def get_apps_router() -> APIRouter:
    app_router = APIRouter(prefix="/api")

    all_routers = [
        auth_router,
        user_router,
        bar_router,
        cocktail_router,
        tag_router,
    ]

    for router in all_routers:
        app_router.include_router(router)

    return app_router
