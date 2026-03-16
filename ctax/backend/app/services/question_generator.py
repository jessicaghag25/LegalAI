from app.schemas.tax import TaxProfileCreate


BASE_QUESTIONS = [
    "Are there carry-forward credits from last year we can still claim?",
    "Should retirement contributions be optimized before filing?",
    "Are provincial/state-specific credits applicable in my case?",
]


def generate_questions(profile: TaxProfileCreate, memory_notes: list[str] | None = None) -> list[str]:
    questions = list(BASE_QUESTIONS)

    if any(src.type == "self_employment" for src in profile.income_sources):
        questions.append("Which business expenses are supportable and least likely to trigger review?")

    if "medical_expenses" in profile.financial_activity:
        questions.append("How should medical expenses be grouped to maximize eligible credits?")

    if profile.dependents:
        questions.append("Which dependent-related benefits and childcare credits can I claim?")

    if any(src.type == "rental_income" for src in profile.income_sources):
        questions.append("Can I claim depreciation/capital cost allowance for rental assets?")

    if memory_notes:
        questions.append("Last year we had missing receipts; what documentation standard should we meet this year?")

    return questions
