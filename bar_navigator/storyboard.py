from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List

from .experience import LearningModule, MultilingualSupport
from .models import Candidate


@dataclass
class StoryboardDay:
    day: str
    title: str
    activities: List[str]

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


class CandidateStoryboardEngine:
    """Builds a day-by-day interactive candidate flow for dashboard rendering."""

    def build(self, candidate: Candidate, modules: List[LearningModule], mentor_note: str) -> List[Dict[str, object]]:
        lang = candidate.profile.preferred_language

        day3_modules = [m.title for m in modules if m.module_type == "knowledge"][:2]
        day4_modules = [m.title for m in modules if m.module_type in {"simulation", "ethics"}][:2]
        day5_modules = [m.title for m in modules if m.module_type in {"soft_skills", "portfolio"}][:2]

        if not day4_modules:
            day4_modules = ["Mock Courtroom Scenario", "Ethics Dilemma Storyline"]
        if not day5_modules:
            day5_modules = ["Negotiation + Empathy Roleplay", "Portfolio Draft Submission"]

        days = [
            StoryboardDay(
                day="Day 1",
                title="Onboarding & Avatar Setup",
                activities=[
                    f"Profile captured for {candidate.profile.name} ({candidate.profile.cultural_background or 'general'} context)",
                    f"Avatar preference set: {candidate.profile.avatar or 'default professional avatar'}",
                    "Welcome dashboard initialized with progress tree and motivational messages",
                ],
            ),
            StoryboardDay(
                day="Day 2",
                title="AI Assessment & Personalized Path",
                activities=[
                    "Assessment engine evaluates strengths, weaknesses, and behavior signals",
                    "Personalized learning path is generated and prioritized",
                    "Visual roadmap displayed in candidate dashboard",
                ],
            ),
            StoryboardDay(
                day="Day 3",
                title="Knowledge Module Engagement",
                activities=[
                    f"Knowledge modules launched: {', '.join(day3_modules) if day3_modules else 'Adaptive knowledge drills'}",
                    "Adaptive micro-questions triggered when weak topics are detected",
                    "Points and badges awarded after completion",
                ],
            ),
            StoryboardDay(
                day="Day 4",
                title="Simulation & Ethics",
                activities=[
                    f"Interactive simulations: {day4_modules[0]}",
                    f"Ethics or judgment module: {day4_modules[-1]}",
                    "AI feedback highlights strengths and areas to improve",
                ],
            ),
            StoryboardDay(
                day="Day 5",
                title="Soft Skills & Portfolio",
                activities=[
                    f"Soft-skills practice: {day5_modules[0]}",
                    f"Portfolio milestone: {day5_modules[-1]}",
                    "AI scoring and improvement suggestions posted to dashboard",
                ],
            ),
            StoryboardDay(
                day="Day 6",
                title="Adaptive Micro-Modules & Reassessment",
                activities=[
                    "Focused drills assigned to weak areas",
                    "Difficulty adapts to candidate performance and pace preference",
                    "AI reassessment updates the learning path",
                ],
            ),
            StoryboardDay(
                day="Day 7",
                title="Mentorship & Mental Health",
                activities=[
                    mentor_note,
                    "Mentor notes integrated into recommendations",
                    MultilingualSupport.translate_text(
                        "Mindfulness prompt and motivational animation displayed", lang
                    ),
                ],
            ),
            StoryboardDay(
                day="Day 8+",
                title="Continuous Loop",
                activities=[
                    "Candidate repeats modules, simulations, and targeted drills",
                    "Progress tree, badges, and story unlocks update cumulatively",
                    "AI continuously personalizes learning and wellbeing support",
                ],
            ),
        ]

        return [d.to_dict() for d in days]
