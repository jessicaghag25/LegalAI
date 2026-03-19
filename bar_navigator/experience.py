from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from .models import Candidate


@dataclass
class LearningModule:
    module_id: str
    title: str
    topic: str
    module_type: str
    difficulty: str = "medium"
    format_type: str = "text"
    language_options: List[str] = field(default_factory=lambda: ["en"])
    prerequisites: List[str] = field(default_factory=list)


class CandidateProgressTracker:
    def track_module_completion(self, candidate: Candidate, module: LearningModule, score: float) -> None:
        candidate.profile.progress[module.module_id] = score

    def award_points(self, candidate: Candidate, points: int) -> None:
        candidate.profile.points += points

    def award_badge(self, candidate: Candidate, badge_name: str) -> None:
        if badge_name not in candidate.profile.badges:
            candidate.profile.badges.append(badge_name)


class ModuleFactory:
    @staticmethod
    def from_learning_path(learning_path: List[str], preferred_language: str) -> List[LearningModule]:
        modules: List[LearningModule] = []
        for index, title in enumerate(learning_path, start=1):
            lowered = title.lower()
            if "ethics" in lowered:
                module_type = "ethics"
            elif "simulation" in lowered or "hearing" in lowered:
                module_type = "simulation"
            elif "portfolio" in lowered:
                module_type = "portfolio"
            elif "negotiation" in lowered or "advocacy" in lowered:
                module_type = "soft_skills"
            else:
                module_type = "knowledge"

            modules.append(
                LearningModule(
                    module_id=f"mod-{index:03d}",
                    title=title,
                    topic=title.split()[0].lower(),
                    module_type=module_type,
                    language_options=[preferred_language, "en"],
                )
            )
        return modules


class AIPersonalizationEngine:
    def analyze_candidate(self, candidate: Candidate) -> Dict[str, List[str]]:
        weak_topics = [topic for topic, score in candidate.performance.topic_scores.items() if score < 70]
        soft_skills_to_improve = [
            name for name, score in candidate.performance.soft_skill_scores.items() if score < 70
        ]
        return {
            "weak_topics": weak_topics,
            "soft_skills_to_improve": soft_skills_to_improve,
        }


class MultilingualSupport:
    supported_languages = ["en", "fr", "es", "pt", "pt-br", "hi", "ur", "gu", "pa", "tl", "ti"]

    @staticmethod
    def translate_text(text: str, target_language: str) -> str:
        if target_language in MultilingualSupport.supported_languages:
            return f"[{target_language}] {text}"
        return text


class MentalHealthSupport:
    prompts = [
        "Take a deep breath and reset your focus.",
        "Progress counts, even when it feels small.",
        "You are building professional confidence every day.",
        "Take a short break, stretch, then re-engage.",
    ]

    def __init__(self, seed: int = 7) -> None:
        self._rng = random.Random(seed)

    def suggest_prompt(self) -> str:
        return self._rng.choice(self.prompts)


class MentorModule:
    def __init__(self) -> None:
        self.sessions: Dict[str, Dict[str, str]] = {}

    def schedule_session(self, candidate: Candidate, mentor_name: str) -> str:
        at = datetime.utcnow().isoformat()
        self.sessions[candidate.profile.candidate_id] = {
            "mentor": mentor_name,
            "scheduled_at": at,
        }
        return f"Mentor {mentor_name} scheduled for {candidate.profile.name} at {at}"


class CandidateDashboard:
    def build_visual_summary(self, candidate: Candidate, recommendations: List[str]) -> Dict[str, object]:
        return {
            "candidate": candidate.profile.name,
            "preferred_language": candidate.profile.preferred_language,
            "progress": candidate.profile.progress,
            "points": candidate.profile.points,
            "badges": candidate.profile.badges,
            "recommendations": recommendations,
            "goal_tracking": candidate.profile.goals,
        }
