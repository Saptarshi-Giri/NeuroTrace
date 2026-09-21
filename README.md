# NeuroTrace

## AI Agent Observability, Trace Analysis and Failure Intelligence

NeuroTrace is an observability and analysis platform for modern AI agents. It is designed to capture multi-step LLM and tool-calling executions as structured traces, analyze token usage and execution behavior, detect repetitive loops and failures, and provide a foundation for understanding and optimizing agent performance.

The project is built around a simple idea:

> Make every step of an AI agent's execution visible, measurable, and analyzable.

## The Idea

Modern AI agents often execute a chain of operations rather than a single model request. A single task may involve multiple LLM calls, tool calls, API requests, database operations, retries, and intermediate decisions.

This makes it difficult to answer questions such as:

- Which step consumed the most tokens?
- Where did the agent spend unnecessary computation?
- Did the agent enter a repetitive loop?
- Which operation caused an execution failure?
- How expensive was a complete agent run?
- What was the actual execution path of the agent?
- Which parts of the execution can be optimized?

NeuroTrace addresses these problems by representing agent executions as structured traces and providing components for trace ingestion, token tracking, loop detection, scoring, and visualization.

The long-term goal is to provide a developer-focused observability layer for AI agent systems that can work with different agent frameworks and execution environments.

## Core Capabilities

### Trace Collection

Capture individual events produced during an agent execution, including:

- LLM calls
- Tool calls
- Execution metadata
- Parent-child relationships
- Inputs and outputs
- Execution order

### Trace Analysis

Analyze collected traces to identify:

- Token consumption
- Expensive execution steps
- Repetitive operations
- Potential execution loops
- Failed operations
- Execution structure

### Agent Performance Intelligence

Transform raw execution data into useful signals through scoring and analysis components.

The architecture is designed to support future capabilities such as:

- Semantic similarity analysis
- Anomaly detection
- Advanced failure classification
- Cost optimization suggestions
- Execution quality metrics

### Agent Framework Testbed

The repository includes an agent testbed for generating representative traces and experimenting with agent frameworks such as:

- CrewAI
- LangGraph

## Tech Stack

### Backend

| Technology | Purpose |
| --- | --- |
| Python 3.11 | Backend and analysis services |
| FastAPI | REST API framework |
| Uvicorn | ASGI application server |
| Pydantic | Data validation and schemas |
| SQLAlchemy | Database ORM |
| SQLite | Local trace persistence |
| Sentence Transformers | Semantic embeddings |
| FAISS | Vector similarity search |

### Frontend

| Technology | Purpose |
| --- | --- |
| React | User interface |
| TypeScript | Type-safe frontend development |
| Vite | Frontend build and development tooling |
| ESLint | Code quality and linting |

### Agent Testbed

| Technology | Purpose |
| --- | --- |
| CrewAI | Agent execution testing |
| LangGraph | Graph-based agent testing |
| Python | Testbed implementation |

## Project Structure

```text
NeuroTrace/
|
|-- agents_testbed/
|   |-- crewai_agent.py
|   |-- generate_sample_trace.py
|   `-- langgraph_agent.py
|
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |   `-- traces.py
|   |   |
|   |   |-- core/
|   |   |
|   |   |-- db/
|   |   |   `-- session.py
|   |   |
|   |   |-- models/
|   |   |   |-- db_models.py
|   |   |   `-- schemas.py
|   |   |
|   |   |-- services/
|   |   |   |-- embeddings/
|   |   |   |
|   |   |   |-- scoring/
|   |   |   |   |-- loop_detector.py
|   |   |   |   `-- token_tracker.py
|   |   |   |
|   |   |   `-- ingestion.py
|   |   |
|   |   `-- main.py
|   |
|   `-- requirements.txt
|
|-- frontend/
|   |-- public/
|   |
|   |-- src/
|   |   |-- api/
|   |   |-- assets/
|   |   |-- components/
|   |   |-- features/
|   |   |   |-- DAGViewer/
|   |   |   `-- TraceList/
|   |   |-- store/
|   |   |-- App.tsx
|   |   `-- main.tsx
|   |
|   |-- package.json
|   |-- package-lock.json
|   |-- tsconfig.json
|   |-- tsconfig.app.json
|   |-- tsconfig.node.json
|   `-- vite.config.ts
|
|-- .gitignore
`-- README.md
```

## Setup Guide

### Prerequisites

Install the following before setting up NeuroTrace:

- Python 3.11
- Node.js 18 or later
- npm
- Git

Python 3.11 is recommended because the project includes machine-learning dependencies such as FAISS and Sentence Transformers.

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/neurotrace.git
cd neurotrace
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

#### Windows

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the backend dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

### 3. Frontend Setup

Open a new terminal and navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

### 4. Run the Agent Testbed

From the project root, make sure the backend virtual environment is active:

```powershell
.\backend\venv\Scripts\Activate.ps1
```

Then run the sample trace generator:

```bash
python agents_testbed/generate_sample_trace.py
```

## Configuration

Environment-specific configuration and secrets should not be committed to the repository.

Use environment variables for values such as API keys and external service credentials.

A local environment file can be created as:

```text
.env
```

For example:

```env
GEMINI_API_KEY=your_api_key
DATABASE_URL=your_database_url
```

Do not commit real credentials or secrets to Git.

## Current Development Status

NeuroTrace is currently under active development.

The repository currently contains the initial backend, frontend, trace ingestion, scoring components, database layer, and agent testbed. Additional observability, analysis, visualization, and production infrastructure capabilities will be added incrementally.

## License

This project is currently under development. A project license will be added before public production distribution.
