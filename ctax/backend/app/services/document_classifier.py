from pathlib import Path


def classify_document(filename: str) -> str:
    name = filename.lower()
    suffix = Path(filename).suffix.lower()

    if any(token in name for token in ["t4", "w2", "income", "paystub"]):
        return "Income Statement"
    if any(token in name for token in ["receipt", "medical", "charity", "donation"]):
        return "Receipt / Deduction Evidence"
    if any(token in name for token in ["trade", "broker", "investment", "1099"]):
        return "Investment Record"
    if suffix == ".csv":
        return "Financial Activity CSV"
    if suffix in {".pdf", ".png", ".jpg", ".jpeg"}:
        return "General Tax Document"
    return "Uncategorized"
