
from fastapi import FastAPI

from {{PROJECT_SLUG}}.interfaces.http.routers.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title={{PROJECT_NAME_LITERAL}})
    app.include_router(health_router)
    return app
