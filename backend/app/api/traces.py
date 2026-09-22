from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.db_models import DBTrace, DBSpan
from app.models.schemas import TraceCreate, SpanCreate
from app.services.scoring.loop_detector import detect_semantic_loops
from app.services.scoring.token_tracker import detect_token_bloat

router = APIRouter(prefix="/v1/traces", tags=["Traces"])

@router.get("", response_model=List[dict])
def list_traces(db: Session = Depends(get_db)):
    traces = db.query(DBTrace).all()
    
    summary = []
    for trace in traces:
        # Count how many spans belong to this trace
        span_count = db.query(DBSpan).filter(DBSpan.trace_id == trace.trace_id).count()
        
        summary.append({
            "trace_id": trace.trace_id,
            "session_id": trace.session_id,
            "total_cost": trace.total_cost,
            "span_count": span_count
        })
        
    return summary

@router.post("", response_model=dict)
def ingest_trace(trace_data: TraceCreate, spans: List[SpanCreate], db: Session = Depends(get_db)):
    total_cost = sum(span.tokens.cost_usd for span in spans if span.tokens)

    # 1. Run the Scoring Engines
    spans_dict = [span.model_dump() for span in spans]
    loop_flags = detect_semantic_loops(spans_dict)
    token_flags = detect_token_bloat(spans_dict)
    
    # Combine flags and group them by span_id
    all_flags = loop_flags + token_flags
    flags_by_span = {}
    for flag in all_flags:
        span_id = flag.pop("span_id")
        if span_id not in flags_by_span:
            flags_by_span[span_id] = []
        flags_by_span[span_id].append(flag)

    # 2. Store Trace
    db_trace = DBTrace(
        trace_id=trace_data.trace_id,
        session_id=trace_data.session_id,
        metadata_json=trace_data.metadata,
        total_cost=total_cost
    )
    db.add(db_trace)

    # 3. Store Spans with their attached AI flags
    for span in spans:
        span_flags = flags_by_span.get(span.span_id, [])
        db_span = DBSpan(
            span_id=span.span_id,
            trace_id=trace_data.trace_id,
            parent_id=span.parent_id,
            name=span.name,
            span_type=span.span_type.value,
            start_time=span.start_time,
            end_time=span.end_time,
            inputs_json=span.inputs,
            outputs_json=span.outputs,
            tokens_json=span.tokens.model_dump() if span.tokens else None,
            flags_json=span_flags
        )
        db.add(db_span)

    db.commit()
    return {"status": "success", "trace_id": trace_data.trace_id, "flags_detected": len(all_flags)}

@router.get("/{trace_id}", response_model=dict)
def get_trace_detail(trace_id: str, db: Session = Depends(get_db)):
    trace = db.query(DBTrace).filter(DBTrace.trace_id == trace_id).first()
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found")

    spans = db.query(DBSpan).filter(DBSpan.trace_id == trace_id).all()
    
    return {
        "trace_id": trace.trace_id,
        "session_id": trace.session_id,
        "metadata": trace.metadata_json,
        "total_cost": trace.total_cost,
        "spans": [
            {
                "span_id": s.span_id,
                "parent_id": s.parent_id,
                "name": s.name,
                "span_type": s.span_type,
                "start_time": s.start_time,
                "end_time": s.end_time,
                "inputs": s.inputs_json,
                "outputs": s.outputs_json,
                "tokens": s.tokens_json,
                "flags": s.flags_json or []
            }
            for s in spans
        ]
    }