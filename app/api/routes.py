"""Endpoints module."""
from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..config import settings
from ..services.rag_pipeline import RAGPipeline
from .schemas import ResponseSchema

app_routes = APIRouter(tags=['auth'])

@app_routes.get('/health-check')
def get_health_check() -> dict:
    """Return status ok."""
    return {
        "status": "OK",
        "env_state": settings.ENV_STATE
    }

@lru_cache(maxsize=1)
def get_rag_pipeline() -> RAGPipeline:
    """Singleton of RAGPipeline."""
    return RAGPipeline()

@app_routes.get('/api/ask', response_model=ResponseSchema)
def get_answer(query: str, rag: Annotated[dict, Depends(get_rag_pipeline)]) -> dict:
    """Generate the answer using RAG."""
    if not query:
        raise HTTPException(status_code=400, detail="No query was provided.")
    answer = rag.generate_answer(query)
    return {"query": query, "answer": answer}
