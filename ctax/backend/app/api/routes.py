from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.tax import (
    AccountantQuestions,
    CelebrationPacket,
    ComplianceEventCreate,
    ComplianceEventResponse,
    ConversationMemory,
    CreditsReport,
    CulturePreferenceUpdate,
    FamilyHubCreate,
    GamificationProgress,
    IntegrationConnection,
    IntegrationConnectionRequest,
    LanguagePreferenceUpdate,
    RiskReport,
    SyncExportRequest,
    SyncEvent,
    SyncImportRequest,
    TaxProfileCreate,
    TaxProfileResponse,
)
from app.services.credit_engine import discover_credits
from app.services.culture_engine import build_celebration_packet, culturally_respectful_tip
from app.services.document_classifier import classify_document
from app.services.gamification import apply_event, mini_games_catalog
from app.services.i18n import (
    DISCLAIMERS,
    GLOSSARY,
    LANGUAGE_DIALECT_HINTS,
    SUPPORTED_LANGUAGES,
    resolve_language,
    tone_prefix,
)
from app.services.integration_engine import (
    SUPPORTED_PROVIDERS,
    export_package,
    import_snapshot,
    provider_oauth_url,
    sync_deadline_reminders,
)
from app.services.memory_engine import memory_highlights
from app.services.question_generator import generate_questions
from app.services.risk_scanner import scan_risks

router = APIRouter(prefix="/api/v1")

PROFILES: dict[str, list[TaxProfileCreate]] = {}
DOCUMENTS: dict[str, list[dict]] = {}
COMPLIANCE_LOGS: dict[str, list[dict]] = {}
FAMILIES: dict[str, FamilyHubCreate] = {}
MEMORIES: dict[str, list[ConversationMemory]] = {}
GAMIFICATION: dict[str, GamificationProgress] = {}
RISK_HISTORY: dict[str, list[dict]] = {}
INTEGRATIONS: dict[str, list[IntegrationConnection]] = {}
SYNC_EVENTS: dict[str, list[SyncEvent]] = {}
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/languages")
def languages():
    return {"languages": SUPPORTED_LANGUAGES, "dialects": LANGUAGE_DIALECT_HINTS}


@router.get("/disclaimer")
def get_disclaimer(lang: str = "en"):
    lang = resolve_language(lang)
    return {"language": lang, "message": DISCLAIMERS[lang]}


@router.get("/glossary")
def glossary():
    return GLOSSARY


@router.get("/integrations/providers")
def integration_providers():
    return {"providers": SUPPORTED_PROVIDERS, "oauth": True, "formats": ["csv", "pdf", "xml", "json"]}


@router.post("/integrations/connect", response_model=IntegrationConnection)
def integration_connect(payload: IntegrationConnectionRequest):
    provider = payload.provider.lower()
    if provider not in SUPPORTED_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    connection = IntegrationConnection(
        connection_id=f"{payload.user_id}:{provider}",
        user_id=payload.user_id,
        family_id=payload.family_id,
        provider=provider,
        status="connected",
        oauth_url=provider_oauth_url(provider, payload.user_id),
        created_at=datetime.utcnow().isoformat(),
    )
    INTEGRATIONS.setdefault(payload.user_id, []).append(connection)
    COMPLIANCE_LOGS.setdefault(payload.user_id, []).append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "Integration Connected",
            "details": {"provider": provider, "oauth": True},
        }
    )
    return connection


@router.get("/integrations/{user_id}")
def integration_list(user_id: str):
    return {"user_id": user_id, "connections": [c.model_dump() for c in INTEGRATIONS.get(user_id, [])]}


@router.post("/integrations/sync/import")
def integration_import(payload: SyncImportRequest):
    snapshot = import_snapshot(payload.provider.lower(), payload.tax_year)
    event = SyncEvent(
        user_id=payload.user_id,
        provider=payload.provider.lower(),
        tax_year=payload.tax_year,
        direction="import",
        status="completed",
        details=snapshot,
    )
    SYNC_EVENTS.setdefault(payload.user_id, []).append(event)

    DOCUMENTS.setdefault(payload.user_id, []).extend(
        [{"filename": name, "category": classify_document(name), "source": payload.provider} for name in snapshot["documents"]]
    )
    COMPLIANCE_LOGS.setdefault(payload.user_id, []).append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "External Import Completed",
            "details": {"provider": payload.provider, "tax_year": payload.tax_year},
        }
    )
    return {"imported": snapshot, "sync_event": event.model_dump()}


@router.post("/integrations/sync/export")
def integration_export(payload: SyncExportRequest):
    if not payload.approval:
        raise HTTPException(status_code=400, detail="User approval required before exporting to tax software")

    profiles = PROFILES.get(payload.user_id, [])
    profile = next((p for p in profiles if p.tax_year == payload.tax_year), None)
    if not profile:
        raise HTTPException(status_code=404, detail="Tax profile not found")

    package = export_package(
        payload.provider.lower(),
        {
            "tax_profile": profile.model_dump(),
            "documents": DOCUMENTS.get(payload.user_id, []),
            "risk_history": RISK_HISTORY.get(payload.user_id, []),
        },
    )
    event = SyncEvent(
        user_id=payload.user_id,
        provider=payload.provider.lower(),
        tax_year=payload.tax_year,
        direction="export",
        status="queued",
        details={"requires_user_approval": False},
    )
    SYNC_EVENTS.setdefault(payload.user_id, []).append(event)
    COMPLIANCE_LOGS.setdefault(payload.user_id, []).append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "External Export Queued",
            "details": {"provider": payload.provider, "tax_year": payload.tax_year},
        }
    )
    return {"export": package, "sync_event": event.model_dump()}


@router.get("/integrations/sync/{user_id}")
def integration_sync_history(user_id: str):
    return {"user_id": user_id, "events": [e.model_dump() for e in SYNC_EVENTS.get(user_id, [])]}


@router.get("/integrations/reminders/{user_id}")
def integration_reminders(user_id: str, region: str = "CA"):
    return {"user_id": user_id, "reminders": sync_deadline_reminders(region)}


@router.post("/family-hub")
def create_family_hub(payload: FamilyHubCreate):
    FAMILIES[payload.family_id] = payload
    return payload


@router.get("/family-hub/{family_id}")
def get_family_hub(family_id: str):
    hub = FAMILIES.get(family_id)
    if not hub:
        raise HTTPException(status_code=404, detail="Family hub not found")

    leaderboard = sorted(
        [p.model_dump() for p in GAMIFICATION.values() if p.family_id == family_id],
        key=lambda x: x["points"],
        reverse=True,
    )
    return {
        "family": hub.model_dump(),
        "leaderboard": leaderboard,
        "mini_games": mini_games_catalog(),
        "animated_tips": [
            "⭐ Respect each member's preferred identity and language while reviewing docs.",
            "🎯 Cross-check carry-forward credits from previous years.",
            "🏆 Cultural celebration theme unlocked for this family's adventure map.",
        ],
        "software_sync": "Connect CRA, TurboTax, BetterTax, H&R Block, or UFile",
        "politically_neutral": True,
    }


@router.post("/preferences/language")
def update_language(payload: LanguagePreferenceUpdate):
    hub = FAMILIES.get(payload.family_id)
    if not hub:
        raise HTTPException(status_code=404, detail="Family hub not found")

    for member in hub.members:
        if member.member_id == payload.member_id:
            member.preferred_language = payload.preferred_language
            return {
                "status": "updated",
                "member_id": payload.member_id,
                "language": payload.preferred_language,
            }

    raise HTTPException(status_code=404, detail="Member not found")


@router.post("/preferences/culture")
def update_culture(payload: CulturePreferenceUpdate):
    hub = FAMILIES.get(payload.family_id)
    if not hub:
        raise HTTPException(status_code=404, detail="Family hub not found")

    for member in hub.members:
        if member.member_id == payload.member_id:
            member.culture = payload.culture
            member.avatar = payload.avatar
            return {"status": "updated", "member_id": payload.member_id, "culture": payload.culture.model_dump()}

    raise HTTPException(status_code=404, detail="Member not found")


@router.get("/celebration/{family_id}/{member_id}", response_model=CelebrationPacket)
def celebration(family_id: str, member_id: str):
    hub = FAMILIES.get(family_id)
    if not hub:
        raise HTTPException(status_code=404, detail="Family hub not found")
    return build_celebration_packet(hub, member_id)


@router.post("/tax-profile", response_model=TaxProfileResponse)
def create_tax_profile(profile: TaxProfileCreate):
    user_profiles = PROFILES.setdefault(profile.user_id, [])
    prior_profiles = [p for p in user_profiles if p.tax_year != profile.tax_year]
    user_profiles.append(profile)

    highlights = memory_highlights(profile, prior_profiles)
    COMPLIANCE_LOGS.setdefault(profile.user_id, []).append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "Tax Profile Created",
            "details": {"tax_year": profile.tax_year, "memory_highlights": highlights},
        }
    )

    progress_key = f"{profile.family_id}:{profile.member_id}"
    progress = GAMIFICATION.setdefault(
        progress_key,
        GamificationProgress(family_id=profile.family_id, member_id=profile.member_id),
    )
    GAMIFICATION[progress_key] = apply_event(progress, "Tax Profile Created")

    return TaxProfileResponse(
        user_id=profile.user_id,
        family_id=profile.family_id,
        member_id=profile.member_id,
        tax_year=profile.tax_year,
        income_sources=[source.model_dump() for source in profile.income_sources],
        dependents=[dependent.model_dump() for dependent in profile.dependents],
        credits_eligibility=[],
        deductions=[],
        documents_uploaded=DOCUMENTS.get(profile.user_id, []),
        memory_highlights=highlights,
    )


@router.post("/credits/discover", response_model=CreditsReport)
def credits_discover(profile: TaxProfileCreate):
    suggestions = discover_credits(profile)
    prior = PROFILES.get(profile.user_id, [])
    recurrent_deductions = (
        sorted(list(set(profile.financial_activity).intersection(*[set(p.financial_activity) for p in prior])))
        if prior
        else []
    )
    hints = ["Review carry-forward balances from prior notices."] if prior else []
    return CreditsReport(
        user_id=profile.user_id,
        tax_year=profile.tax_year,
        potential_credits=suggestions,
        recurrent_deductions=recurrent_deductions,
        unused_credit_hints=hints,
    )


@router.post("/risk/scan", response_model=RiskReport)
def risk_scan(profile: TaxProfileCreate):
    has_documents = bool(DOCUMENTS.get(profile.user_id))
    score, warnings, explainability = scan_risks(profile, has_documents)
    RISK_HISTORY.setdefault(profile.user_id, []).append({"tax_year": profile.tax_year, "risk_score": score})

    COMPLIANCE_LOGS.setdefault(profile.user_id, []).append(
        {"timestamp": datetime.utcnow().isoformat(), "event": "Risk Scan Performed", "details": {"score": score}}
    )

    return RiskReport(
        user_id=profile.user_id,
        tax_year=profile.tax_year,
        risk_score=score,
        warnings=warnings,
        explainability=explainability,
        cumulative_risk_trend=RISK_HISTORY.get(profile.user_id, []),
    )


@router.post("/documents/upload")
async def upload_document(user_id: str, family_id: str, member_id: str, file: UploadFile = File(...)):
    content = await file.read()
    target = UPLOAD_DIR / f"{user_id}_{file.filename}"
    target.write_bytes(content)

    category = classify_document(file.filename)
    item = {
        "filename": file.filename,
        "category": category,
        "mime_type": file.content_type,
        "stored_as": str(target),
        "ocr_language_support": list(SUPPORTED_LANGUAGES.keys()),
        "linked_deductions": ["education", "medical_expenses", "charitable_donations"],
    }
    DOCUMENTS.setdefault(user_id, []).append(item)
    COMPLIANCE_LOGS.setdefault(user_id, []).append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "Document Upload Completed",
            "details": {"filename": file.filename, "category": category},
        }
    )

    progress_key = f"{family_id}:{member_id}"
    progress = GAMIFICATION.setdefault(
        progress_key,
        GamificationProgress(family_id=family_id, member_id=member_id),
    )
    GAMIFICATION[progress_key] = apply_event(progress, "Document Upload Completed")

    return {"uploaded": file.filename, "category": category}


@router.post("/questions/generate", response_model=AccountantQuestions)
def questions_generate(profile: TaxProfileCreate):
    prior = [p for p in PROFILES.get(profile.user_id, []) if p.tax_year != profile.tax_year]
    questions = generate_questions(profile, memory_highlights(profile, prior))
    return AccountantQuestions(user_id=profile.user_id, tax_year=profile.tax_year, questions=questions)


@router.post("/memory/conversation")
def add_memory(payload: ConversationMemory):
    MEMORIES.setdefault(payload.user_id, []).append(payload)
    return payload


@router.get("/memory/{user_id}")
def get_memory(user_id: str):
    return {"user_id": user_id, "history": [m.model_dump() for m in MEMORIES.get(user_id, [])]}


@router.post("/games/complete")
def complete_game(family_id: str, member_id: str, game_name: str):
    progress_key = f"{family_id}:{member_id}"
    progress = GAMIFICATION.setdefault(
        progress_key,
        GamificationProgress(family_id=family_id, member_id=member_id),
    )
    GAMIFICATION[progress_key] = apply_event(progress, "Mini-Game Completed")

    COMPLIANCE_LOGS.setdefault(family_id, []).append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "Mini-Game Completed",
            "details": {"game": game_name, "points": GAMIFICATION[progress_key].points},
        }
    )
    return GAMIFICATION[progress_key]


@router.get("/gamification/{family_id}")
def family_gamification(family_id: str):
    entries = [g.model_dump() for g in GAMIFICATION.values() if g.family_id == family_id]
    total_points = sum(e["points"] for e in entries)
    return {
        "family_id": family_id,
        "collective_points": total_points,
        "achievements": sorted({badge for e in entries for badge in e["badges"]}),
        "members": sorted(entries, key=lambda e: e["points"], reverse=True),
        "adventure_map": [
            {"level": 1, "title": "Profile Pioneer", "unlock_at": 0},
            {"level": 2, "title": "Receipt Ranger", "unlock_at": 100},
            {"level": 3, "title": "Risk Reducer", "unlock_at": 200},
            {"level": 4, "title": "Family Tax Hero", "unlock_at": 350},
        ],
    }


@router.post("/compliance/log", response_model=ComplianceEventResponse)
def compliance_log(event: ComplianceEventCreate):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event.event,
        "details": event.details,
    }
    COMPLIANCE_LOGS.setdefault(event.user_id, []).append(log)
    return ComplianceEventResponse(user_id=event.user_id, family_id=event.family_id, event=event.event, details=event.details)


@router.get("/compliance/log/{user_id}")
def compliance_log_list(user_id: str):
    return {"user_id": user_id, "events": COMPLIANCE_LOGS.get(user_id, [])}


@router.get("/tips/{family_id}/{member_id}")
def contextual_tips(family_id: str, member_id: str, region: str = "CA"):
    hub = FAMILIES.get(family_id)
    if not hub:
        raise HTTPException(status_code=404, detail="Family hub not found")
    member = next((m for m in hub.members if m.member_id == member_id), None)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return {
        "tone": tone_prefix(member.culture.tone),
        "tips": [
            culturally_respectful_tip(region, member.preferred_language),
            "Double-check missing receipts from prior years before final review.",
        ],
    }


@router.get("/summary/export/{user_id}/{tax_year}")
def export_summary(user_id: str, tax_year: str):
    profiles = PROFILES.get(user_id, [])
    profile = next((p for p in profiles if p.tax_year == tax_year), None)
    if not profile:
        raise HTTPException(status_code=404, detail="Tax profile not found")

    prior = [p for p in profiles if p.tax_year != tax_year]
    credits = [c.model_dump() for c in discover_credits(profile)]
    score, warnings, explainability = scan_risks(profile, has_documents=bool(DOCUMENTS.get(user_id)))
    memory = memory_highlights(profile, prior)
    questions = generate_questions(profile, memory)

    return {
        "user_id": user_id,
        "family_id": profile.family_id,
        "tax_year": profile.tax_year,
        "tax_profile": profile.model_dump(),
        "documents": DOCUMENTS.get(user_id, []),
        "potential_credits": credits,
        "risk_report": {
            "risk_score": score,
            "warnings": warnings,
            "explainability": explainability,
            "trend": RISK_HISTORY.get(user_id, []),
        },
        "memory_highlights": memory,
        "questions_for_accountant": questions,
        "conversation_memory": [m.model_dump() for m in MEMORIES.get(user_id, [])],
        "gamification": [g.model_dump() for g in GAMIFICATION.values() if g.family_id == profile.family_id],
        "integrations": [c.model_dump() for c in INTEGRATIONS.get(user_id, [])],
        "sync_history": [e.model_dump() for e in SYNC_EVENTS.get(user_id, [])],
        "compliance_log": COMPLIANCE_LOGS.get(user_id, []),
        "disclaimers": DISCLAIMERS,
        "politically_neutral": True,
    }
