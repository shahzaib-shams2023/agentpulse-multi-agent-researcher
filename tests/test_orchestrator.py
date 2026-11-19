import asyncio
from app.models.schemas import ResearchRequest
from app.orchestrator import MultiAgentOrchestrator


def test_full_orchestration_pipeline():
    async def run():
        orchestrator = MultiAgentOrchestrator()
        req = ResearchRequest(query="Agentic Workflows ReAct vs Multi-Agent DAGs", depth="deep")
        return await orchestrator.execute_research(req)

    result = asyncio.run(run())
    assert result.request.query == "Agentic Workflows ReAct vs Multi-Agent DAGs"
    assert len(result.plan.tasks) >= 4
    assert len(result.evidence_gathered) > 0
    assert result.critic_review.confidence_score > 0.5
    assert len(result.logs) == 4
    assert result.elapsed_seconds >= 0.0
    assert "Executive Summary" in result.final_report.markdown_content
