from app.schemas.tax import GamificationProgress

BADGE_THRESHOLDS = {
    "Starter": 50,
    "Organizer": 120,
    "Family Champion": 250,
    "Tax Detective": 400,
}


EVENT_POINTS = {
    "Tax Profile Created": 20,
    "Document Upload Completed": 15,
    "Risk Scan Performed": 10,
    "Mini-Game Completed": 30,
    "Quiz Completed": 25,
}


def apply_event(progress: GamificationProgress, event: str) -> GamificationProgress:
    progress.points += EVENT_POINTS.get(event, 5)
    progress.level = max(1, progress.points // 100 + 1)

    for badge, threshold in BADGE_THRESHOLDS.items():
        if progress.points >= threshold and badge not in progress.badges:
            progress.badges.append(badge)

    return progress


def mini_games_catalog() -> list[dict[str, str]]:
    return [
        {
            "name": "Receipt Matcher",
            "audience": "family",
            "description": "Match receipts to categories for points.",
        },
        {
            "name": "Deduction Detective",
            "audience": "adult",
            "description": "Identify potential deductions hidden in scenarios.",
        },
        {
            "name": "Family Tax Quiz",
            "audience": "family",
            "description": "Team challenge on prior-year tax decisions and best practices.",
        },
    ]
