import uuid
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# Update this URL if your SQLite database is named differently
SQLALCHEMY_DATABASE_URL = "sqlite:///./traces.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Minimal ORM models to ensure we can insert data
class DBTrace(Base):
    __tablename__ = "traces"
    trace_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    total_cost = Column(Float, default=0.0)
    metadata_json = Column(JSON)

class DBSpan(Base):
    __tablename__ = "spans"
    span_id = Column(String, primary_key=True, index=True)
    trace_id = Column(String, index=True)
    parent_id = Column(String, nullable=True)
    name = Column(String)
    span_type = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, default=datetime.utcnow)
    inputs_json = Column(JSON)
    outputs_json = Column(JSON)
    tokens_json = Column(JSON)
    flags_json = Column(JSON)

Base.metadata.create_all(bind=engine)
db = SessionLocal()

def create_sample():
    trace_id = f"trace-{uuid.uuid4().hex[:8]}"
    
    # 1. Create Trace
    trace = DBTrace(
        trace_id=trace_id,
        session_id="session-test-01",
        total_cost=0.042,
        metadata_json={"env": "development", "agent_version": "1.0.3"}
    )
    db.add(trace)

    # 2. Root Agent Span
    root_id = str(uuid.uuid4())
    root_span = DBSpan(
        span_id=root_id, trace_id=trace_id, parent_id=None,
        name="ResearchAgent", span_type="agent",
        inputs_json={"goal": "Analyze market trends"}, outputs_json={"status": "completed"},
        flags_json=[]
    )
    db.add(root_span)

    # 3. LLM Reasoning Span
    llm_id = str(uuid.uuid4())
    llm_span = DBSpan(
        span_id=llm_id, trace_id=trace_id, parent_id=root_id,
        name="GPT-4-Turbo", span_type="llm",
        inputs_json={"prompt": "Determine next steps"}, outputs_json={"completion": "Call search tool"},
        flags_json=[]
    )
    db.add(llm_span)

    # 4. First Tool Call (Normal)
    tool1_id = str(uuid.uuid4())
    tool1_span = DBSpan(
        span_id=tool1_id, trace_id=trace_id, parent_id=root_id,
        name="WebSearchTool", span_type="tool",
        inputs_json={"query": "Q3 market report"}, outputs_json={"results": "Found 5 documents"},
        flags_json=[]
    )
    db.add(tool1_span)

    # 5. Second Tool Call (Flagged as Semantic Loop)
    tool2_id = str(uuid.uuid4())
    tool2_span = DBSpan(
        span_id=tool2_id, trace_id=trace_id, parent_id=root_id,
        name="WebSearchTool", span_type="tool",
        inputs_json={"query": "Q3 market report 2026"}, outputs_json={"results": "Found 5 documents"},
        flags_json=[{
            "flag_type": "Semantic Loop", 
            "severity": "high", 
            "message": "98% similar to previous tool call. Redundant action detected by FAISS."
        }]
    )
    db.add(tool2_span)

    db.commit()
    print(f"✅ Successfully inserted trace: {trace_id}")

if __name__ == "__main__":
    create_sample()