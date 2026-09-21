from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class DBTrace(Base):
    __tablename__ = "traces"

    trace_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    metadata_json = Column(JSON, nullable=True)
    total_cost = Column(Float, default=0.0)

    spans = relationship("DBSpan", back_populates="trace", cascade="all, delete-orphan")

class DBSpan(Base):
    __tablename__ = "spans"

    span_id = Column(String, primary_key=True, index=True)
    trace_id = Column(String, ForeignKey("traces.trace_id"), nullable=False)
    parent_id = Column(String, nullable=True)
    name = Column(String, nullable=False)
    span_type = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    inputs_json = Column(JSON, nullable=True)
    outputs_json = Column(JSON, nullable=True)
    tokens_json = Column(JSON, nullable=True)
    flags_json = Column(JSON, nullable=True)

    trace = relationship("DBTrace", back_populates="spans")