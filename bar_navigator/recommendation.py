from __future__ import annotations

from typing import List

from .models import AssessmentResult, Candidate, Recommendation


class RecommendationEngine:
    def suggest_next_steps(self, candidate: Candidate, assessment: AssessmentResult) -> List[Recommendation]:
        recommendations: List[Recommendation] = []

        for idx, module in enumerate(candidate.learning_path[:5], start=1):
            recommendations.append(
                Recommendation(
                    item_type="study_module",
                    title=module,
                    rationale="Addresses high-priority weakness identified by AI assessment.",
                    priority=idx,
                )
            )

        for flag in assessment.behavioral_flags:
            if flag == "timed_exam_performance":
                recommendations.append(
                    Recommendation(
                        item_type="timed_simulation",
                        title="90-minute timed mixed-topic simulation",
                        rationale="Improves performance under exam time pressure.",
                        priority=1,
                    )
                )
            elif flag == "focus_management":
                recommendations.append(
                    Recommendation(
                        item_type="coaching",
                        title="Focus and stamina micro-session with mentor",
                        rationale="Targets sustained attention and study cadence.",
                        priority=2,
                    )
                )
            elif flag == "confidence_and_test_anxiety":
                recommendations.append(
                    Recommendation(
                        item_type="mentorship",
                        title="One-on-one confidence coaching",
                        rationale="Supports exam resilience after repeated attempts.",
                        priority=2,
                    )
                )

        unique = {(r.item_type, r.title): r for r in recommendations}
        return sorted(unique.values(), key=lambda rec: rec.priority)[:6]
