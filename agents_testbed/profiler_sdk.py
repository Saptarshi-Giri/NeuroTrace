import requests
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class AgentProfiler:
    def __init__(self, api_url: str = "http://127.0.0.1:8000/v1/traces", session_id: str = "default_session"):
        self.api_url = api_url
        self.session_id = session_id
        self.trace_id = f"trace_{uuid.uuid4().hex[:8]}"
        self.spans: List[Dict[str, Any]] = []

    def add_span(
        self,
        name: str,
        span_type: str,  # 'agent', 'llm', or 'tool'
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        parent_id: Optional[str] = None,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        cost_usd: float = 0.0
    ) -> str:
        span_id = f"span_{uuid.uuid4().hex[:6]}"
        now = datetime.now(timezone.utc).isoformat()
        
        span_data = {
            "span_id": span_id,
            "parent_id": parent_id,
            "name": name,
            "span_type": span_type,
            "start_time": now,
            "end_time": now,
            "inputs": inputs,
            "outputs": outputs,
            "tokens": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
                "cost_usd": cost_usd
            }
        }
        self.spans.append(span_data)
        return span_id

    def flush(self):
        """Sends collected trace and spans to the profiler backend."""
        payload = {
            "trace_data": {
                "trace_id": self.trace_id,
                "session_id": self.session_id,
                "metadata": {"sdk_version": "0.1.0"}
            },
            "spans": self.spans
        }
        res = requests.post(self.api_url, json=payload)
        return res.json()