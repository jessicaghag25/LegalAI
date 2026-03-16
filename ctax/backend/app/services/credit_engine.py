from app.schemas.tax import CreditSuggestion, TaxProfileCreate


EDUCATION_KEYWORDS = {"education", "tuition"}
MEDICAL_KEYWORDS = {"medical_expenses"}
HOME_KEYWORDS = {"home_ownership", "first_time_homebuyer"}
CHARITY_KEYWORDS = {"charitable_donations"}


def discover_credits(profile: TaxProfileCreate) -> list[CreditSuggestion]:
    activities = set(profile.financial_activity)
    suggestions: list[CreditSuggestion] = []

    if activities.intersection(EDUCATION_KEYWORDS):
        suggestions.append(
            CreditSuggestion(
                name="Education Credit",
                reason="Tuition or education expenses were indicated.",
                explainability="Education-related costs often qualify for tuition credits.",
            )
        )

    if activities.intersection(MEDICAL_KEYWORDS):
        suggestions.append(
            CreditSuggestion(
                name="Medical Expense Credit",
                reason="Medical expenses were reported.",
                explainability=(
                    "Medical expenses over threshold may qualify for non-refundable credits."
                ),
            )
        )

    if activities.intersection(HOME_KEYWORDS):
        suggestions.append(
            CreditSuggestion(
                name="Home Buyer / Ownership Credit",
                reason="Home ownership activity was reported.",
                explainability="Home-related credits may apply depending on timing and jurisdiction.",
            )
        )

    if activities.intersection(CHARITY_KEYWORDS):
        suggestions.append(
            CreditSuggestion(
                name="Charitable Donation Credit",
                reason="Charitable donations were indicated.",
                explainability="Receipted charitable donations may generate tax credits.",
            )
        )

    if any(source.type == "self_employment" for source in profile.income_sources):
        suggestions.append(
            CreditSuggestion(
                name="Business Expense Deductions",
                reason="Self-employment income was reported.",
                explainability="Business-use expenses may be deductible with support documentation.",
            )
        )

    return suggestions
