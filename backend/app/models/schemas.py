from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SpanType(str, Enum):
    AGENT = "agent"      # The overarching agent reasoning loop
    LLM = "llm"          # A direct call to an LLM (OpenAI, Anthropic)
    TOOL = "tool"        # A function call (e.g., search_web, read_file)

class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0

class ProfilerFlag(BaseModel):
    flag_type: str       # e.g., "semantic_loop", "token_bloat", "redundant_tool"
    severity: str        # "warning", "critical"
    message: str

class SpanCreate(BaseModel):
    span_id: str
    parent_id: Optional[str] = None
    name: str
    span_type: SpanType
    start_time: datetime
    end_time: Optional[datetime] = None
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    tokens: Optional[TokenUsage] = None

class SpanResponse(SpanCreate):
    flags: List[ProfilerFlag] = Field(default_factory=list)

class TraceCreate(BaseModel):
    trace_id: str
    session_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TraceResponse(TraceCreate):
    spans: List[SpanResponse] = Field(default_factory=list)
    total_cost: float = 0.0