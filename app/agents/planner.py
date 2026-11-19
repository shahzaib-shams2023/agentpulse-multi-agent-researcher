import json
import re
from typing import List
from app.agents.base import BaseAgent
from app.models.schemas import ResearchRequest, ResearchPlan, SubTask


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PlannerAgent",
            role="Research Strategist responsible for decomposing questions into structured hypotheses and search tasks"
        )

    async def create_plan(self, request: ResearchRequest) -> ResearchPlan:
        system_prompt = (
            "You are a Principal Research Architect. Decompose the user's research topic into a structured research plan. "
            "Return valid JSON with keys: 'core_hypotheses' (list of strings), and 'tasks' (list of objects with "
            "'id', 'question', 'target_keywords', 'rationale')."
        )
        user_prompt = f"Topic: {request.query}\nDepth: {request.depth}\nDomain: {request.domain_filter or 'general'}"

        raw_response = await self.call_llm(system_prompt, user_prompt)
        return self._parse_or_build_plan(raw_response, request)

    def _parse_or_build_plan(self, raw_text: str, request: ResearchRequest) -> ResearchPlan:
        try:
            # Check for JSON block
            json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                tasks = [SubTask(**t) for t in data.get("tasks", [])]
                if tasks:
                    return ResearchPlan(
                        original_query=request.query,
                        core_hypotheses=data.get("core_hypotheses", [f"Analysis of {request.query}"]),
                        tasks=tasks,
                        estimated_steps=len(tasks)
                    )
        except Exception:
            pass

        # Robust deterministic plan generation
        keywords = [word.lower() for word in re.findall(r"\w+", request.query) if len(word) > 3]
        tasks = [
            SubTask(
                id=1,
                question=f"What are the foundational architectures and key definitions regarding {request.query}?",
                target_keywords=keywords[:3] or ["architecture", "overview"],
                rationale="Establish baseline technical context and operational taxonomy."
            ),
            SubTask(
                id=2,
                question=f"What are the quantitative performance benchmarks, latency tradeoffs, and resource costs for {request.query}?",
                target_keywords=keywords + ["performance", "benchmark", "tradeoffs"],
                rationale="Evaluate quantitative engineering metrics and constraints."
            ),
            SubTask(
                id=3,
                question=f"What are the primary operational failure modes, security considerations, and edge cases?",
                target_keywords=keywords + ["security", "edge-cases", "failures"],
                rationale="Identify production reliability risks and failure mitigations."
            )
        ]
        if request.depth == "deep":
            tasks.append(
                SubTask(
                    id=4,
                    question=f"What is the industry trajectory and recommended production adoption roadmap?",
                    target_keywords=keywords + ["roadmap", "adoption", "future"],
                    rationale="Formulate actionable deployment guidance."
                )
            )

        return ResearchPlan(
            original_query=request.query,
            core_hypotheses=[
                f"Architecture selection around '{request.query}' is heavily governed by latency vs scalability tradeoffs.",
                f"Production readiness requires balancing operational simplicity against distributed system overhead."
            ],
            tasks=tasks,
            estimated_steps=len(tasks)
        )

