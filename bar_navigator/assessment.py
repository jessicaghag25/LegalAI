from __future__ import annotations

from statistics import mean
from typing import List

from .models import AssessmentResult, Candidate


class AIAssessmentEngine:
    """Heuristic assessment engine that can later be replaced with ML models."""

    WEAKNESS_THRESHOLD = 70
    STRENGTH_THRESHOLD = 85

    def analyze(self, candidate: Candidate) -> AssessmentResult:
        topic_scores = candidate.performance.topic_scores
        strengths = [topic for topic, score in topic_scores.items() if score >= self.STRENGTH_THRESHOLD]
        weaknesses = [topic for topic, score in topic_scores.items() if score < self.WEAKNESS_THRESHOLD]

        repeated_error_topics = [
            topic for topic, score in topic_scores.items() if score < 60
        ]

        behavioral_flags = self._behavioral_flags(candidate)

        readiness = self._readiness_score(candidate, weaknesses, behavioral_flags)
        pass_probability = max(0.0, min(1.0, readiness / 100.0))

        return AssessmentResult(
            strengths=strengths,
            weaknesses=weaknesses,
            repeated_error_topics=repeated_error_topics,
            behavioral_flags=behavioral_flags,
            readiness_score=round(readiness, 2),
            pass_probability=round(pass_probability, 2),
        )

    def _behavioral_flags(self, candidate: Candidate) -> List[str]:
        flags: List[str] = []
        if candidate.performance.average_focus_minutes < 25:
            flags.append("focus_management")

        mock_avg = mean(candidate.performance.mock_exam_scores) if candidate.performance.mock_exam_scores else 0
        if mock_avg < 65:
            flags.append("timed_exam_performance")

        if candidate.profile.prior_exam_attempts >= 2:
            flags.append("confidence_and_test_anxiety")

        return flags

    def _readiness_score(self, candidate: Candidate, weaknesses: List[str], behavioral_flags: List[str]) -> float:
        topic_mean = mean(candidate.performance.topic_scores.values()) if candidate.performance.topic_scores else 0
        mock_mean = mean(candidate.performance.mock_exam_scores) if candidate.performance.mock_exam_scores else 0
        portfolio_mean = mean(candidate.performance.portfolio_scores.values()) if candidate.performance.portfolio_scores else 0

        score = (topic_mean * 0.5) + (mock_mean * 0.35) + (portfolio_mean * 0.15)
        score -= len(weaknesses) * 1.5
        score -= len(behavioral_flags) * 2
        return max(0.0, min(100.0, score))
