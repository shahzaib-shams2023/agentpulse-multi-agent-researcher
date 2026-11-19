import time
from typing import List
from app.models.schemas import (
    ResearchRequest,
    FullResearchResponse,
    AgentExecutionLog
)
from app.tools.search_engine import SearchEngine
from app.agents.planner import PlannerAgent
from app.agents.researcher import ResearchAgent
from app.agents.critic import CriticAgent
from app.agents.synthesizer import SynthesizerAgent


class MultiAgentOrchestrator:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent(self.search_engine)
        self.critic = CriticAgent()
        self.synthesizer = SynthesizerAgent()

    async def execute_research(self, request: ResearchRequest) -> FullResearchResponse:
        start_time = time.time()
        logs: List[AgentExecutionLog] = []

        # Step 1: Planning
        logs.append(AgentExecutionLog(
            step_number=1,
            agent_name=self.planner.name,
            action="Decomposing research query and formulating hypotheses",
            details={"query": request.query, "depth": request.depth}
        ))
        plan = await self.planner.create_plan(request)

        # Step 2: Information Gathering
        logs.append(AgentExecutionLog(
            step_number=2,
            agent_name=self.researcher.name,
            action="Querying search index and gathering authoritative evidence",
            details={"task_count": len(plan.tasks)}
        ))
        evidence = await self.researcher.gather_evidence(plan)

        # Step 3: Verification & Auditing
        logs.append(AgentExecutionLog(
            step_number=3,
            agent_name=self.critic.name,
            action="Auditing evidence, detecting contradictions, and scoring confidence",
            details={"evidence_sources_evaluated": len(evidence)}
        ))
        critic_review = await self.critic.evaluate_evidence(plan, evidence)

        # Step 4: Executive Synthesis
        logs.append(AgentExecutionLog(
            step_number=4,
            agent_name=self.synthesizer.name,
            action="Synthesizing final executive briefing with markdown and inline citations",
            details={"confidence_score": critic_review.confidence_score}
        ))
        final_report = await self.synthesizer.compile_report(plan, evidence, critic_review)

        elapsed = round(time.time() - start_time, 3)
        return FullResearchResponse(
            request=request,
            plan=plan,
            evidence_gathered=evidence,
            critic_review=critic_review,
            final_report=final_report,
            logs=logs,
            elapsed_seconds=elapsed
        )

