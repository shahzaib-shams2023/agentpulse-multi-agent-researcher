from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
import os

from app.models.schemas import ResearchRequest, FullResearchResponse
from app.orchestrator import MultiAgentOrchestrator
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Autonomous Multi-Agent Research & Synthesis Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = MultiAgentOrchestrator()
history: List[FullResearchResponse] = []

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "AgentPulse Multi-Agent Research System API is running."}


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.environment,
        "llm_mode": "online" if settings.llm_api_key else "offline-simulation"
    }


@app.post("/api/research", response_model=FullResearchResponse)
async def conduct_research(request: ResearchRequest):
    try:
        response = await orchestrator.execute_research(request)
        history.append(response)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research execution failed: {str(e)}")


@app.get("/api/history", response_model=List[FullResearchResponse])
async def get_research_history():
    return history[-10:]

