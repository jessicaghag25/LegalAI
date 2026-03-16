from datetime import datetime, timedelta
from typing import Any

SUPPORTED_PROVIDERS = {
    "cra": "CRA My Account / NETFILE",
    "turbotax": "TurboTax",
    "bettertax": "BetterTax",
    "hrblock": "H&R Block",
    "ufile": "UFile",
}


def provider_oauth_url(provider: str, user_id: str) -> str:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError("Unsupported provider")
    return f"https://connect.ctax.local/oauth/{provider}?user_id={user_id}&scope=read_write_tax"


def import_snapshot(provider: str, tax_year: str) -> dict[str, Any]:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError("Unsupported provider")
    return {
        "provider": provider,
        "tax_year": tax_year,
        "income_sources": [
            {"type": "employment", "amount": 64000},
            {"type": "investment", "amount": 1200},
        ],
        "deductions": ["rrsp", "medical_expenses"],
        "credits": ["tuition_carry_forward"],
        "documents": ["T4_imported.pdf", "rrsp_receipt_imported.pdf"],
        "risk_alerts": ["missing_medical_receipt"],
        "imported_at": datetime.utcnow().isoformat(),
    }


def export_package(provider: str, payload: dict[str, Any]) -> dict[str, Any]:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError("Unsupported provider")
    return {
        "provider": provider,
        "status": "queued_for_push",
        "requires_user_approval": True,
        "format_options": ["json", "csv", "xml", "pdf"],
        "payload_preview": payload,
    }


def sync_deadline_reminders(region: str = "CA") -> list[dict[str, str]]:
    now = datetime.utcnow().date()
    return [
        {
            "title": "Tax filing deadline reminder",
            "due_date": str(now + timedelta(days=20)),
            "region": region,
        },
        {
            "title": "Document verification checkpoint",
            "due_date": str(now + timedelta(days=10)),
            "region": region,
        },
    ]
