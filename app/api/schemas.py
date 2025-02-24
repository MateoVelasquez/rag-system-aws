"""API Pydantic schemes."""
from pydantic import BaseModel


class ResponseSchema(BaseModel):
    """Schema for API response."""
    query: str
    answer: str
