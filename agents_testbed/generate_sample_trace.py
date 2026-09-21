import requests
from datetime import datetime, timezone

API_URL = "http://127.0.0.1:8000/v1/traces"

now = datetime.now(timezone.utc).isoformat()

payload = {
    "trace_data": {
        "trace_id": "trace_001",
        "session_id": "sess_100",
        "metadata": {"agent_framework": "langgraph", "environment": "dev"}
    },
    "spans": [
        {
            "span_id": "span_root",
            "parent_id": None,
            "name": "ResearchAgent",
            "span_type": "agent",
            "start_time": now,
            "end_time": now,
            "inputs": {"query": "Find population of Odisha"},
            "outputs": {"status": "completed"},
            "tokens": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150, "cost_usd": 0.002}
        },
        {
            "span_id": "span_tool_1",
            "parent_id": "span_root",
            "name": "wikipedia_search",
            "span_type": "tool",
            "start_time": now,
            "end_time": now,
            "inputs": {"search_term": "Population of Odisha"},
            "outputs": {"result": "41.9 Million"},
            "tokens": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "cost_usd": 0.0}
        }
    ]
}

response = requests.post(API_URL, json=payload)
print("Response Status:", response.status_code)
print("Response JSON:", response.json())