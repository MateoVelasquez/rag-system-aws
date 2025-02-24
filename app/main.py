"""RAG System app."""
from fastapi import FastAPI

from .api.routes import app_routes
from .config import settings


def register_routers(app: FastAPI) -> None:
    """Register routes in app."""
    app.include_router(app_routes)

def create_app() -> FastAPI:
    """App factory."""
    app = FastAPI(
        title='RAG SYSTEM AWS: Service',
        description='Service',
        docs_url=settings.DOCS_URL
    )
    register_routers(app)
    return app

# APP creation
app = create_app()
