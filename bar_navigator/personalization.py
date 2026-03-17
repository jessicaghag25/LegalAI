from __future__ import annotations

from typing import Dict, List

from .models import Candidate


MODULE_CATALOG: Dict[str, Dict[str, str]] = {
    "contracts": {
        "visual": "Contracts Concept Map + Video Drills",
        "auditory": "Contracts Audio Issue-Spotting Session",
        "reading/writing": "Contracts Case-Law Reading Pack",
        "kinesthetic": "Contracts Simulation Drafting Workshop",
    },
    "criminal": {
        "visual": "Criminal Law Flowcharts + Timelines",
        "auditory": "Criminal Law Oral Recitation Group",
        "reading/writing": "Criminal Law Statutory Interpretation Workbook",
        "kinesthetic": "Criminal Law Mock Hearing Simulation",
    },
    "ethics": {
        "visual": "Professional Ethics Decision Tree Module",
        "auditory": "Ethics Podcast + Mentor Reflection",
        "reading/writing": "Ethics Rule Comparison Workbook",
        "kinesthetic": "Ethics Client-Interview Roleplay",
    },
}


class PersonalizationLayer:
    def generate_learning_path(self, candidate: Candidate, weaknesses: List[str]) -> List[str]:
        style = candidate.profile.learning_style.lower()
        generated: List[str] = []

        for topic in weaknesses:
            topic_catalog = MODULE_CATALOG.get(topic.lower())
            if topic_catalog:
                module = topic_catalog.get(style) or topic_catalog.get("reading/writing")
            else:
                module = f"Adaptive {topic.title()} Intensive Module"

            if candidate.profile.neurodiversity_supports:
                module += " (with accessibility supports)"

            generated.append(module)

        candidate.learning_path = generated
        return generated
