from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine, Base
from app.api.traces import router as traces_router

# Auto-create SQLite database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agent Trace Profiler API",
    description="Observability layer for LLM Agent pipelines",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoints
app.include_router(traces_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "agent-trace-profiler"}