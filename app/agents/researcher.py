from typing import List
from app.agents.base import BaseAgent
from app.models.schemas import ResearchPlan, SourceEvidence
from app.tools.search_engine import SearchEngine


class ResearchAgent(BaseAgent):
    def __init__(self, search_engine: SearchEngine):
        super().__init__(
            name="ResearchAgent",
            role="Information Retrieval Specialist responsible for querying search tools and gathering authoritative evidence"
        )
        self.search_engine = search_engine

    async def gather_evidence(self, plan: ResearchPlan) -> List[SourceEvidence]:
        all_evidence: List[SourceEvidence] = []
        seen_ids = set()

        for task in plan.tasks:
            query_str = f"{task.question} {' '.join(task.target_keywords)}"
            results = self.search_engine.search(query_str, limit=3)
            for item in results:
                if item.source_id not in seen_ids:
                    seen_ids.add(item.source_id)
                    all_evidence.append(item)

        return all_evidence

