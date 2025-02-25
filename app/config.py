"""API config module."""
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())

DOCS_URL = "/docs"

class DefaultSettings(BaseSettings):
    """General config."""
    # ENV STATE:
    ENV_STATE: str = 'default'
    # APP_CONFIG
    BASE_DIR: Path = Path(__file__).parent.parent
    SECRET_KEY: str = ''
    # DOCS
    DOCS_URL: str | None = None

    # AWS CONFIG:
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_DEFAULT_REGION: str = "us-east-2"

    AWS_OPENSEARCH_HOST: str = ""
    AWS_OPENSEARCH_PORT: int = 443
    AWS_OPENSEARCH_USER: str = ""
    AWS_OPENSEARCH_PASSWORD: str = ""

    AWS_OPENSEARCH_INDEX_NAME: str = "rag_system_index"

    # EMBEDDING:
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # LLM:
    LLM_MODEL: str = "llama3"
    LLM_PROMPT: str = """You are an AI assistant specialized in providing accurate
    and context-aware responses.

    Context:
    {context}

    Question:
    {question}

    Instructions:
    - Answer concisely and directly based on the provided context.
    - If the context lacks information, indicate it instead of making assumptions.
    - Use clear and structured language to improve readability.

    Answer:"""

    # WIKIPEDIA API
    WIKI_USER_AGENT: str = "RAG-system-aws/1.0 (email: mavemo2604@gmail.com)"
    WIKI_USER_LANGUAGE: str = "en"

    # S3
    S3_BUCKET_NAME: str = "rag-system-s3-bucket"

    class Config:  # noqa: D106
        env_file = ".env"


class LocalDevSettings(DefaultSettings):
    """Config for local ENV."""
    # ENV CONFIG
    ENV_STATE: str = "localdev"
    DEBUG_MODE: bool = True
    # DOCS
    DOCS_URL: str | None = DOCS_URL


class DevSettings(DefaultSettings):
    """Config for develop ENV."""
    # ENV CONFIG
    ENV_STATE: str = "dev"
    DEBUG_MODE: bool = True
    # DOCS
    DOCS_URL: str | None = DOCS_URL
    # MODEL
    LLM_MODEL: str = "qwen2.5:0.5b"


def get_settings() -> BaseSettings:
    """Define config by ENV."""
    env_state = os.getenv("ENV_STATE", "localdev")
    if env_state == "dev":
        return DevSettings()
    return LocalDevSettings()

settings = get_settings()
