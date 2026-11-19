# AgentPulse: Autonomous Multi-Agent Research & Synthesis Engine

AgentPulse is an asynchronous multi-agent research platform designed to decompose complex analytical questions, query information tools, audit claims for factual contradictions, and synthesize cited executive briefings.

---

## 🔍 The Problem
Modern knowledge workers and engineering leaders face cognitive overload when synthesizing technical decisions. Relying on single-prompt LLM outputs frequently produces shallow summaries, unverified hallucinated citations, and missed architectural nuances. Single-shot models lack the iterative reflection and separation of concerns necessary for thorough research.

## 💡 The Solution
AgentPulse deploys a directed acyclic multi-agent architecture where four specialized agents collaborate with distinct responsibilities:
1. **PlannerAgent**: Deconstructs high-level queries into verifiable technical hypotheses and targeted sub-tasks.
2. **ResearchAgent**: Executes focused keyword and semantic retrieval against knowledge sources, gathering concrete citations.
3. **CriticAgent**: Audits findings, detects logical contradictions, checks for vendor bias, and calculates an empirical factuality confidence score.
4. **SynthesizerAgent**: Compiles a comprehensive executive briefing formatted in Markdown with bracketed source citations `[SRC-ID]`.

---

## 🏛️ System Architecture

```
User Query
    │
    ▼
[PlannerAgent] ───► Deconstructs into Sub-tasks & Hypotheses
    │
    ▼
[ResearchAgent] ──► Multi-Query Knowledge & Web Retrieval
    │
    ▼
[CriticAgent] ───► Contradiction Detection & Confidence Scoring
    │
    ▼
[SynthesizerAgent]► Executive Briefing Generation with Inline Citations
    │
    ▼
REST API / Interactive Dashboard
```

---

## 🛠️ Technology Stack
- **Backend**: Python 3.11, FastAPI, Pydantic v2, AsyncIO, HTTPX
- **Testing**: Pytest, Pytest-AsyncIO, Starlette TestClient
- **Frontend**: Responsive Single-Page Application (Tailwind CSS, FontAwesome, Marked.js)
- **Deployment**: Docker, Docker Compose, GitHub Actions CI
- **AI Integrations**: OpenAI-compatible API client with deterministic offline simulation engine

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Git

### Installation
```bash
# Navigate to project directory
cd agentpulse-multi-agent-researcher

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
To connect a live LLM, set `LLM_API_KEY` (e.g., from OpenAI, Groq, or OpenRouter). If left blank, AgentPulse operates automatically in offline simulation mode.

### Running the Application
```bash
python -m uvicorn app.main:app --reload --port 8000
```
Open `http://localhost:8000` in your browser to access the interactive web interface, or `http://localhost:8000/docs` for the OpenAPI documentation.

---

## 🧪 Running Automated Tests
Run the complete test suite:
```bash
pytest tests/ -v
```

---

## 🐳 Docker Deployment
```bash
# Build and run with Docker Compose
docker compose up --build
```
The application will be live at `http://localhost:8000`.

---

## 📡 API Reference

### Conduct Research
`POST /api/research`
```json
{
  "query": "SQLite vs DuckDB for edge analytics workloads",
  "depth": "standard",
  "domain_filter": "engineering"
}
```

Response:
```json
{
  "request": { "query": "..." },
  "plan": { "core_hypotheses": [...], "tasks": [...] },
  "evidence_gathered": [
    { "source_id": "KB-SQL-01", "title": "...", "reliability_score": 0.95 }
  ],
  "critic_review": {
    "verified_claims": [...],
    "confidence_score": 0.92
  },
  "final_report": {
    "title": "Executive Research Briefing: ...",
    "markdown_content": "# Executive Research Briefing..."
  },
  "elapsed_seconds": 0.42
}
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

