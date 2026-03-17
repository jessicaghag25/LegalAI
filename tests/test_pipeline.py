from bar_navigator.models import Candidate, CandidatePerformance, CandidateProfile
from bar_navigator.pipeline import BarNavigatorService


def test_full_pipeline_generates_outputs():
    candidate = Candidate(
        profile=CandidateProfile(
            candidate_id="cand-001",
            name="Avery",
            experience_years=1,
            prior_exam_attempts=2,
            learning_style="visual",
            neurodiversity_supports=["extended_time"],
            cultural_background="multilingual",
            target_practice_area="criminal",
            preferred_language="fr",
            goals=["Pass bar exam", "Improve advocacy"],
            avatar="professional_avatar_01",
            pace_preference="flexible",
        ),
        performance=CandidatePerformance(
            topic_scores={"contracts": 62, "criminal": 58, "ethics": 72},
            soft_skill_scores={"advocacy": 70, "negotiation": 66},
            ethics_score=72,
            mock_exam_scores=[59, 63, 65],
            portfolio_scores={"memo": 68, "argument": 64},
            average_focus_minutes=22,
        ),
    )

    output = BarNavigatorService().run(candidate)

    assert "assessment" in output
    assert "learning_path" in output
    assert "recommendations" in output
    assert "personalization_analysis" in output
    assert "mental_health_prompt" in output
    assert "storyboard" in output
    assert output["assessment"]["pass_probability"] <= 1.0
    assert len(output["learning_path"]) >= 1
    assert any(r["item_type"] == "timed_simulation" for r in output["recommendations"])
    assert output["mental_health_prompt"].startswith("[fr]")
    assert output["candidate_dashboard"]["points"] >= 10
    assert output["storyboard"][0]["day"] == "Day 1"
    assert output["storyboard"][-1]["day"] == "Day 8+"
