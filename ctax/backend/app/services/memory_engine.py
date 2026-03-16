from app.schemas.tax import TaxProfileCreate


def memory_highlights(current: TaxProfileCreate, prior_profiles: list[TaxProfileCreate]) -> list[str]:
    if not prior_profiles:
        return ["No prior year memory yet. Complete this year to build your annual memory trail."]

    highlights: list[str] = []
    prior_activities = [set(p.financial_activity) for p in prior_profiles]
    recurrent = set.intersection(*prior_activities) if prior_activities else set()

    if recurrent:
        highlights.append(
            f"Recurring activity detected: {', '.join(sorted(recurrent))}. Confirm if these apply this year."
        )

    prior_risks = [
        "missing_receipts"
        for p in prior_profiles
        if "missing_receipts" in p.financial_activity or "medical_expenses" in p.financial_activity
    ]
    if prior_risks:
        highlights.append(
            "Previously flagged documentation gaps were seen. Upload receipts early this year."
        )

    if any("education" in p.financial_activity for p in prior_profiles) and "education" not in current.financial_activity:
        highlights.append("Last year education deductions appeared. Should we check if tuition applies again?")

    highlights.append("Context-aware follow-up: Last year you claimed deductions. Do they apply again this year?")
    return highlights
