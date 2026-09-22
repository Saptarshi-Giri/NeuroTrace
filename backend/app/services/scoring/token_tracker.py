from typing import List, Dict, Any

def detect_token_bloat(spans: List[Dict[str, Any]], max_tokens_per_step: int = 4000) -> List[Dict[str, Any]]:
    """Flags any LLM or Tool call that exceeds a healthy token threshold."""
    flags = []
    
    for span in spans:
        tokens = span.get("tokens")
        if not tokens:
            continue
            
        total = tokens.get("total_tokens", 0)
        if total > max_tokens_per_step:
            flags.append({
                "span_id": span["span_id"],
                "flag_type": "token_bloat",
                "severity": "warning",
                "message": f"High token usage detected: {total} tokens in a single step."
            })
            
    return flags