from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CandidateProfile:
    candidate_id: str
    name: str
    experience_years: int
    prior_exam_attempts: int
    learning_style: str
    cultural_background: str = ""
    neurodiversity_supports: List[str] = field(default_factory=list)
    target_practice_area: str = "general"
    preferred_language: str = "en"
    age: Optional[int] = None
    gender: str = ""
    avatar: Optional[str] = None
    goals: List[str] = field(default_factory=list)
    pace_preference: str = "normal"
    progress: Dict[str, float] = field(default_factory=dict)
    points: int = 0
    badges: List[str] = field(default_factory=list)


@dataclass
class CandidatePerformance:
    topic_scores: Dict[str, float]
    soft_skill_scores: Dict[str, float]
    ethics_score: float
    mock_exam_scores: List[float]
    portfolio_scores: Dict[str, float]
    average_focus_minutes: int


@dataclass
class Candidate:
    profile: CandidateProfile
    performance: CandidatePerformance
    learning_path: List[str] = field(default_factory=list)


@dataclass
class AssessmentResult:
    strengths: List[str]
    weaknesses: List[str]
    repeated_error_topics: List[str]
    behavioral_flags: List[str]
    readiness_score: float
    pass_probability: float


@dataclass
class Recommendation:
    item_type: str
    title: str
    rationale: str
    priority: int


@dataclass
class CandidateSnapshot:
    candidate_name: str
    topic_mastery: Dict[str, float]
    soft_skills: Dict[str, float]
    ethics_score: float
    module_completion_rate: float
    readiness_score: float
    pass_probability: float
