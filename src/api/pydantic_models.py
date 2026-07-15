"""Request and response models for the rag-multimodal-2026 API."""

from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field


class QueryInput(BaseModel):
    question: str
    session_id: Optional[str] = None
    model: str = Field(
        default="gpt-4o-mini",
        description=(
            "Model name. Routed by name: gpt uses OpenAI, claude uses Anthropic, "
            "and llama, qwen, deepseek, mistral, gemma, or phi use local Ollama."
        ),
    )


class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: str
    steps: list = []
    images: list = []
    sources: list = []


class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: Union[datetime, str]


class DeleteFileRequest(BaseModel):
    file_id: int
