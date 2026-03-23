from typing import Optional

from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="required, non-empty")
    max_length: int = Field(default=100, gt=0, description="optional, default 100")


class SummarizeResponse(BaseModel):
    summary: str
    model: str
    truncated: bool


class SummaryRow(BaseModel):
    id: int
    input_text: str
    summary_text: str
    model: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    latency_ms: Optional[int] = None
    created_at: str
