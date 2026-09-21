<div align="center">

# NeuroTrace

### Observability, Trace Analysis & Failure Intelligence for AI Agents

**See inside every decision your AI agents make.**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-frontend-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Status](https://img.shields.io/badge/status-active%20development-orange)](#current-development-status)
[![License](https://img.shields.io/badge/license-TBD-lightgrey)](#license)

[Overview](#overview) • [Features](#core-capabilities) • [Architecture](#architecture) • [Quick Start](#quick-start) • [Roadmap](#roadmap) • [Contributing](#contributing)

</div>

---

## Overview

Modern AI agents rarely make a single model call — they **chain** LLM calls, tool invocations, API requests, database operations, and retries into complex, multi-step executions. When something goes wrong (or gets expensive, or loops forever), most teams are left debugging blind.

**NeuroTrace** turns opaque agent executions into structured, queryable, visual traces — so you can answer the questions that actually matter:

- 💸 Which step consumed the most tokens?
- 🔁 Did the agent get stuck in a repetitive loop?
- 🐌 Where is execution time or cost being wasted?
- ❌ Which operation caused the failure?
- 🧩 What was the agent's actual execution path?
- 📊 How much did this run cost, end to end?

> **The idea is simple:** make every step of an AI agent's execution visible, measurable, and analyzable.

---

## Core Capabilities

<table>
<tr>
<td width="33%" valign="top">

### 📥 Trace Collection
Capture every event in an agent's execution — LLM calls, tool calls, parent-child relationships, inputs/outputs, execution order, and metadata — as structured, replayable traces.

</td>
<td width="33%" valign="top">

### 🔍 Trace Analysis
Break down token consumption, surface the most expensive steps, detect repetitive operations and potential loops, flag failed operations, and map execution structure.

</td>
<td width="33%" valign="top">

### 📈 Performance Intelligence
Convert raw execution data into actionable signals through scoring, loop detection, and analysis components built for extensibility.

</td>
</tr>
</table>

**On the roadmap:** semantic similarity analysis, anomaly detection, advanced failure classification, automated cost-optimization suggestions, and execution quality metrics.

### 🧪 Agent Framework Testbed

NeuroTrace ships with a built-in testbed for generating realistic traces against popular agent frameworks, including:

- **CrewAI**
- **LangGraph**

This makes it easy to validate NeuroTrace against real agent behavior — or to use as a reference implementation for instrumenting your own framework.

---

## Architecture

NeuroTrace is a full-stack platform, cleanly separated into three layers:

| Layer | Role |
|---|---|
| **Agent Testbed** | Generates representative execution traces from real agent frameworks (CrewAI, LangGraph) |
| **Backend** | Ingests, stores, and analyzes traces via a FastAPI service backed by SQLAlchemy/SQLite, with vector search for semantic analysis |
| **Frontend** | Visualizes execution as an interactive DAG, with trace browsing and inspection tooling |

### Tech Stack

<table>
<tr>
<td valign="top">

**Backend**

| Technology | Purpose |
|---|---|
| Python 3.11 | Core services |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Pydantic | Validation & schemas |
| SQLAlchemy | Database ORM |
| SQLite | Local trace persistence |
| Sentence Transformers | Semantic embeddings |
| FAISS | Vector similarity search |

</td>
<td valign="top">

**Frontend**

| Technology | Purpose |
|---|---|
| React | UI framework |
| TypeScript | Type-safe development |
| Vite | Build & dev tooling |
| ESLint | Code quality |

</td>
<td valign="top">

**Agent Testbed**

| Technology | Purpose |
|---|---|
| CrewAI | Agent execution testing |
| LangGraph | Graph-based agent testing |
| Python | Testbed implementation |

</td>
</tr>
</table>

### Project Structure

```text
NeuroTrace/
├── agents_testbed/
│   ├── crewai_agent.py
│   ├── generate_sample_trace.py
│   └── langgraph_agent.py
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── traces.py
│   │   ├── core/
│   │   ├── db/
│   │   │   └── session.py
│   │   ├── models/
│   │   │   ├── db_models.py
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   ├── embeddings/
│   │   │   ├── scoring/
│   │   │   │   ├── loop_detector.py
│   │   │   │   └── token_tracker.py
│   │   │   └── ingestion.py
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── DAGViewer/
│   │   │   └── TraceList/
│   │   ├── store/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── .gitignore
└── README.md
```

---

## Quick Start

### Prerequisites

- **Python 3.11** *(required — needed for FAISS and Sentence Transformers compatibility)*
- **Node.js 18+**
- **npm**
- **Git**

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/neurotrace.git
cd neurotrace
```

### 2. Set up the backend

```bash
cd backend

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install -r requirements.txt

# Launch the API server
uvicorn app.main:app --reload
```

| Service | URL |
|---|---|
| API | http://127.0.0.1:8000 |
| Interactive docs (Swagger) | http://127.0.0.1:8000/docs |

### 3. Set up the frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The app will be available at **http://localhost:5173**.

### 4. Generate sample traces

With the backend virtual environment active, from the project root:

```bash
python agents_testbed/generate_sample_trace.py
```

This runs a sample agent execution through the testbed and feeds real trace data into NeuroTrace — the fastest way to see the platform in action.

---

## Configuration

Secrets and environment-specific values are kept out of version control. Create a local `.env` file in the backend directory:

```env
GEMINI_API_KEY=your_api_key
DATABASE_URL=your_database_url
```

> ⚠️ Never commit real credentials or API keys to the repository.

---

## Roadmap

- [ ] Semantic similarity analysis across traces
- [ ] Anomaly detection for execution outliers
- [ ] Advanced failure classification
- [ ] Automated cost-optimization suggestions
- [ ] Execution quality scoring
- [ ] Broader agent framework support beyond CrewAI / LangGraph
- [ ] Production deployment guide

## Current Development Status

🚧 **NeuroTrace is under active development.**

The repository currently includes the initial backend, frontend, trace ingestion pipeline, scoring components, database layer, and agent testbed. Additional observability, analysis, visualization, and production-readiness features are being added incrementally.

Feedback, issues, and ideas are welcome as the project takes shape.

## Contributing

Contributions, bug reports, and feature suggestions are welcome. If you're interested in AI agent observability and want to help shape the project's direction, feel free to open an issue or start a discussion.

## License

This project is currently under development. A license will be added prior to public production distribution.

---

<div align="center">
<sub>Built for developers who want to see what their AI agents are actually doing.</sub>
</div>
