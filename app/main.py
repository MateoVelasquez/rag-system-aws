"""RAG System app."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import __version__
from .api.routes import app_routes
from .config import settings


def register_routers(app: FastAPI) -> None:
    """Register routes in app."""
    app.include_router(app_routes)

def create_app() -> FastAPI:
    """App factory."""
    app = FastAPI(
        title='RAG SYSTEM AWS: Service',
        description=(
            "This service implements a Retrieval-Augmented Generation (RAG) system "
            "that extracts information from Wikipedia on topics related to IT, "
            "software development, machine learning, and artificial intelligence. "
            "It processes user queries and generates accurate, contextualized answers."
        ),
        docs_url=settings.DOCS_URL,
        version=__version__
    )
    # routers
    register_routers(app)
    # static
    app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")
    return app

# APP creation
app = create_app()
