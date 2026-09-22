import requests
import uuid
from datetime import datetime, timezone

API_URL = "http://127.0.0.1:8000/v1/traces"
now = datetime.now(timezone.utc).isoformat()

# Generate unique IDs
trace_id = f"trace_{uuid.uuid4().hex[:6]}"
root_span_id = f"span_root_{uuid.uuid4().hex[:4]}"
llm_span_id = f"span_llm_{uuid.uuid4().hex[:4]}"

payload = {
    "trace_data": {
        "trace_id": trace_id,
        "session_id": "sess_100",
        "metadata": {"agent_framework": "langgraph", "environment": "dev"}
    },
    "spans": [
        # 1. Root Agent
        {
            "span_id": root_span_id,
            "parent_id": None,
            "name": "ResearchAgent",
            "span_type": "agent",
            "start_time": now,
            "end_time": now,
            "inputs": {"query": "Find population of Odisha"},
            "outputs": {"status": "completed"},
            "tokens": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "cost_usd": 0.0}
        },
        # 2. LLM Reasoning (Triggering Token Bloat with 8500 tokens)
        {
            "span_id": llm_span_id,
            "parent_id": root_span_id,
            "name": "GPT-4-Turbo",
            "span_type": "llm",
            "start_time": now,
            "end_time": now,
            "inputs": {"system_prompt": "You are a research agent...", "context": "Massive retrieved document..."},
            "outputs": {"thought": "I should search Wikipedia for the population."},
            "tokens": {"prompt_tokens": 8000, "completion_tokens": 500, "total_tokens": 8500, "cost_usd": 0.09}
        },
        # 3. First Tool Call
        {
            "span_id": f"span_tool_1_{uuid.uuid4().hex[:4]}",
            "parent_id": llm_span_id,
            "name": "wikipedia_search",
            "span_type": "tool",
            "start_time": now,
            "end_time": now,
            "inputs": {"search_term": "Population of Odisha"},
            "outputs": {"result": "41.9 Million"},
            "tokens": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "cost_usd": 0.0}
        },
        # 4. Second Tool Call (Triggering Semantic Loop Flag)
        {
            "span_id": f"span_tool_2_{uuid.uuid4().hex[:4]}",
            "parent_id": llm_span_id,
            "name": "wikipedia_search",
            "span_type": "tool",
            "start_time": now,
            "end_time": now,
            "inputs": {"search_term": "How many people live in Odisha"},
            "outputs": {"result": "41.9 Million"},
            "tokens": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "cost_usd": 0.0}
        }
    ]
}

response = requests.post(API_URL, json=payload)
print("Response Status:", response.status_code)
print("Response JSON:", response.json())