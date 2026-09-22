from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Any

# Loads a lightweight, local, CPU-optimized embedding model
# (Downloads ~80MB into cache on the very first run)
model = SentenceTransformer("all-MiniLM-L6-v2")

def detect_semantic_loops(spans: List[Dict[str, Any]], similarity_threshold: float = 0.90) -> List[Dict[str, Any]]:
    """Uses vector embeddings to detect if an agent is repeatedly asking the same semantic question."""
    flags = []
    
    # Filter for tool spans (where looping behavior is most obvious and costly)
    tool_spans = [s for s in spans if s.get("span_type") == "tool"]
    
    if len(tool_spans) < 2:
        return flags
        
    # Extract the tool inputs to embed
    texts_to_embed = [str(span.get("inputs", {})) for span in tool_spans]
    
    # Generate vectors
    embeddings = model.encode(texts_to_embed)
    embeddings = np.array(embeddings).astype("float32")
    
    # Normalize vectors so the Inner Product calculates Cosine Similarity
    faiss.normalize_L2(embeddings)
    
    # Build a rapid FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension) 
    index.add(embeddings)
    
    # Scan spans for high similarity against previous steps in the chain
    for i, span in enumerate(tool_spans):
        if i == 0: 
            continue
            
        current_vector = embeddings[i:i+1]
        # Query the index for the top (i+1) matches
        distances, indices = index.search(current_vector, k=i+1)
        
        for j, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            # If a highly similar match occurred BEFORE the current step, it's a loop
            if idx < i and dist >= similarity_threshold:
                flags.append({
                    "span_id": span["span_id"],
                    "flag_type": "semantic_loop",
                    "severity": "critical",
                    "message": f"Semantic loop detected: Tool input is {dist:.1%} similar to previous span '{tool_spans[idx]['name']}'."
                })
                break # Only flag the current span once
                
    return flags