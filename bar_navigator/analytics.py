from __future__ import annotations

from statistics import mean

from .models import AssessmentResult, Candidate, CandidateSnapshot


class AnalyticsReporter:
    def build_candidate_snapshot(self, candidate: Candidate, assessment: AssessmentResult) -> CandidateSnapshot:
        topic_mastery = candidate.performance.topic_scores
        completed_modules = sum(1 for m in candidate.learning_path if "Adaptive" not in m)
        completion_rate = (completed_modules / len(candidate.learning_path) * 100) if candidate.learning_path else 0

        return CandidateSnapshot(
            candidate_name=candidate.profile.name,
            topic_mastery=topic_mastery,
            soft_skills=candidate.performance.soft_skill_scores,
            ethics_score=candidate.performance.ethics_score,
            module_completion_rate=round(completion_rate, 2),
            readiness_score=assessment.readiness_score,
            pass_probability=assessment.pass_probability,
        )

    def improvement_trend(self, historical_mock_scores: list[float]) -> float:
        if len(historical_mock_scores) < 2:
            return 0.0
        midpoint = len(historical_mock_scores) // 2
        first_half = mean(historical_mock_scores[:midpoint])
        second_half = mean(historical_mock_scores[midpoint:])
        return round(second_half - first_half, 2)
