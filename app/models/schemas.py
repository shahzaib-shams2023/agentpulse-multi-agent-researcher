from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=5, description="Primary research question or topic")
    depth: str = Field("standard", description="Research depth: standard or deep")
    domain_filter: Optional[str] = Field(None, description="Optional domain focus (e.g., engineering, finance, security)")


class SubTask(BaseModel):
    id: int
    question: str
    target_keywords: List[str]
    rationale: str
    status: str = "pending"


class ResearchPlan(BaseModel):
    original_query: str
    core_hypotheses: List[str]
    tasks: List[SubTask]
    estimated_steps: int


class SourceEvidence(BaseModel):
    source_id: str
    title: str
    url: str
    content: str
    reliability_score: float = 0.95
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class CriticEvaluation(BaseModel):
    verified_claims: List[str]
    potential_biases: List[str]
    contradictions_detected: List[str]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    recommendations_for_synthesizer: str


class ExecutiveReport(BaseModel):
    title: str
    executive_summary: str
    key_findings: List[Dict[str, Any]]
    comparative_analysis: Optional[Dict[str, Any]] = None
    confidence_score: float
    sources: List[SourceEvidence]
    markdown_content: str
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class AgentExecutionLog(BaseModel):
    step_number: int
    agent_name: str
    action: str
    details: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class FullResearchResponse(BaseModel):
    request: ResearchRequest
    plan: ResearchPlan
    evidence_gathered: List[SourceEvidence]
    critic_review: CriticEvaluation
    final_report: ExecutiveReport
    logs: List[AgentExecutionLog]
    elapsed_seconds: float

