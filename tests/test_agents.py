import asyncio
from app.models.schemas import ResearchRequest
from app.agents.planner import PlannerAgent
from app.agents.researcher import ResearchAgent
from app.agents.critic import CriticAgent
from app.agents.synthesizer import SynthesizerAgent
from app.tools.search_engine import SearchEngine


def test_planner_agent_creates_valid_plan():
    async def run():
        planner = PlannerAgent()
        req = ResearchRequest(query="SQLite vs DuckDB performance in edge analytics", depth="standard")
        return await planner.create_plan(req)

    plan = asyncio.run(run())
    assert plan.original_query == "SQLite vs DuckDB performance in edge analytics"
    assert len(plan.tasks) >= 3
    assert len(plan.core_hypotheses) >= 1
    assert all(t.question for t in plan.tasks)


def test_researcher_agent_gathers_evidence():
    async def run():
        engine = SearchEngine()
        researcher = ResearchAgent(engine)
        planner = PlannerAgent()
        req = ResearchRequest(query="Microservices vs Modular Monolith", depth="standard")
        plan = await planner.create_plan(req)
        return await researcher.gather_evidence(plan)

    evidence = asyncio.run(run())
    assert len(evidence) > 0
    assert all(e.source_id and e.title for e in evidence)


def test_critic_agent_audits_evidence():
    async def run():
        critic = CriticAgent()
        planner = PlannerAgent()
        engine = SearchEngine()
        researcher = ResearchAgent(engine)
        req = ResearchRequest(query="Zero Trust Security Architecture", depth="standard")
        plan = await planner.create_plan(req)
        evidence = await researcher.gather_evidence(plan)
        return await critic.evaluate_evidence(plan, evidence)

    evaluation = asyncio.run(run())
    assert 0.0 <= evaluation.confidence_score <= 1.0
    assert len(evaluation.verified_claims) > 0
    assert evaluation.recommendations_for_synthesizer


def test_synthesizer_agent_compiles_executive_report():
    async def run():
        planner = PlannerAgent()
        engine = SearchEngine()
        researcher = ResearchAgent(engine)
        critic = CriticAgent()
        synthesizer = SynthesizerAgent()

        req = ResearchRequest(query="Vector Databases HNSW vs Distributed", depth="standard")
        plan = await planner.create_plan(req)
        evidence = await researcher.gather_evidence(plan)
        critic_eval = await critic.evaluate_evidence(plan, evidence)
        return await synthesizer.compile_report(plan, evidence, critic_eval), critic_eval, evidence

    report, critic_eval, evidence = asyncio.run(run())
    assert report.title.startswith("Executive Research Briefing")
    assert "Executive Summary" in report.markdown_content
    assert len(report.sources) == len(evidence)
    assert report.confidence_score == critic_eval.confidence_score
