"""Endpoints module."""
from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, responses
from fastapi.templating import Jinja2Templates

from ..config import settings
from ..services.rag_pipeline import RAGPipeline
from .schemas import QuerySchema, ResponseSchema

app_routes = APIRouter(tags=['RAG'])
templates = Jinja2Templates(directory="app/templates")

@app_routes.get("/", response_class=responses.HTMLResponse)
def home(request: Request) -> None:
    """Index page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app_routes.get('/app_info')
def get_health_check() -> dict:
    """Return status ok."""
    return {
        "status": "OK",
        "env_state": settings.ENV_STATE,
        "llm_model": settings.LLM_MODEL,
        "developer": 'Mateo Velásquez',
        "email": 'mateo10velasquez@hotmail.com',
    }

@lru_cache(maxsize=1)
def get_rag_pipeline() -> RAGPipeline:
    """Singleton of RAGPipeline."""
    return RAGPipeline()

@app_routes.post('/api/ask', response_model=ResponseSchema)
def get_answer(
    query: QuerySchema,
    rag: Annotated[dict, Depends(get_rag_pipeline)]
) -> dict:
    """Generate the answer using RAG."""
    query_dump = query.model_dump()
    question = query_dump.get('question', None)
    if not question:
        raise HTTPException(status_code=400, detail="No query was provided.")
    answer = rag.generate_answer(question)
    return {"query": question, "answer": answer}
