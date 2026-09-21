from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.db_models import DBTrace, DBSpan
from app.models.schemas import TraceCreate, TraceResponse, SpanCreate

router = APIRouter(prefix="/v1/traces", tags=["Traces"])

@router.post("", response_model=dict)
def ingest_trace(trace_data: TraceCreate, spans: List[SpanCreate], db: Session = Depends(get_db)):
    # Calculate initial total cost across all spans
    total_cost = sum(span.tokens.cost_usd for span in spans if span.tokens)

    # 1. Store Trace
    db_trace = DBTrace(
        trace_id=trace_data.trace_id,
        session_id=trace_data.session_id,
        metadata_json=trace_data.metadata,
        total_cost=total_cost
    )
    db.add(db_trace)

    # 2. Store Spans
    for span in spans:
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
            flags_json=[]
        )
        db.add(db_span)

    db.commit()
    return {"status": "success", "trace_id": trace_data.trace_id, "spans_ingested": len(spans)}

@router.get("", response_model=List[dict])
def list_traces(db: Session = Depends(get_db)):
    traces = db.query(DBTrace).all()
    return [
        {
            "trace_id": t.trace_id,
            "session_id": t.session_id,
            "total_cost": t.total_cost,
            "span_count": len(t.spans)
        }
        for t in traces
    ]