from app.schemas.tax import TaxProfileCreate


def scan_risks(profile: TaxProfileCreate, has_documents: bool = False) -> tuple[int, list[str], list[str]]:
    score = 100
    warnings: list[str] = []
    explainability: list[str] = []

    if not has_documents:
        score -= 25
        warnings.append("Missing receipt/document upload evidence.")
        explainability.append("No supporting files were uploaded for claims validation.")

    total_income = sum(source.amount for source in profile.income_sources)
    if total_income <= 0:
        score -= 30
        warnings.append("Income appears incomplete or zero.")
        explainability.append("Income reporting is required for complete tax diagnostics.")

    if "vehicle_expense_high" in profile.financial_activity:
        score -= 20
        warnings.append("High vehicle expense claim indicated.")
        explainability.append("Vehicle claims are commonly reviewed and require usage records.")

    if any(source.type == "rental" for source in profile.income_sources) and (
        "rental_expense_log" not in profile.financial_activity
    ):
        score -= 10
        warnings.append("Rental income reported without rental expense log activity.")
        explainability.append("Rental filings typically need expense and occupancy documentation.")

    score = max(0, min(100, score))
    return score, warnings, explainability
