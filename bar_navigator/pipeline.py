from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from .analytics import AnalyticsReporter
from .assessment import AIAssessmentEngine
from .experience import (
    AIPersonalizationEngine,
    CandidateDashboard,
    CandidateProgressTracker,
    MentalHealthSupport,
    MentorModule,
    ModuleFactory,
    MultilingualSupport,
)
from .models import Candidate
from .storyboard import CandidateStoryboardEngine
from .personalization import PersonalizationLayer
from .recommendation import RecommendationEngine


class BarNavigatorService:
    def __init__(self) -> None:
        self.assessment_engine = AIAssessmentEngine()
        self.personalization_layer = PersonalizationLayer()
        self.recommendation_engine = RecommendationEngine()
        self.analytics = AnalyticsReporter()
        self.ai_personalization_engine = AIPersonalizationEngine()
        self.progress_tracker = CandidateProgressTracker()
        self.mentor_module = MentorModule()
        self.dashboard = CandidateDashboard()
        self.wellbeing = MentalHealthSupport()
        self.storyboard_engine = CandidateStoryboardEngine()

    def run(self, candidate: Candidate) -> Dict[str, Any]:
        assessment = self.assessment_engine.analyze(candidate)
        learning_path = self.personalization_layer.generate_learning_path(candidate, assessment.weaknesses)
        recommendations = self.recommendation_engine.suggest_next_steps(candidate, assessment)
        snapshot = self.analytics.build_candidate_snapshot(candidate, assessment)

        modules = ModuleFactory.from_learning_path(learning_path, candidate.profile.preferred_language)
        for module in modules[:2]:
            baseline_score = candidate.performance.topic_scores.get(module.topic, 70)
            self.progress_tracker.track_module_completion(candidate, module, baseline_score)
            self.progress_tracker.award_points(candidate, 10)

        if assessment.pass_probability < 0.65:
            mentor_note = self.mentor_module.schedule_session(candidate, mentor_name="Assigned Mentor")
        else:
            mentor_note = "No urgent mentor intervention required."

        analysis = self.ai_personalization_engine.analyze_candidate(candidate)
        wellbeing_prompt = MultilingualSupport.translate_text(
            self.wellbeing.suggest_prompt(), candidate.profile.preferred_language
        )
        dashboard = self.dashboard.build_visual_summary(
            candidate,
            recommendations=[r.title for r in recommendations],
        )
        storyboard = self.storyboard_engine.build(candidate, modules, mentor_note)

        return {
            "assessment": asdict(assessment),
            "learning_path": learning_path,
            "recommendations": [asdict(r) for r in recommendations],
            "dashboard_snapshot": asdict(snapshot),
            "personalization_analysis": analysis,
            "modules": [asdict(m) for m in modules],
            "mentor_intervention": mentor_note,
            "mental_health_prompt": wellbeing_prompt,
            "candidate_dashboard": dashboard,
            "storyboard": storyboard,
        }
