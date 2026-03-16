from typing import Any, Literal

from pydantic import BaseModel, Field


SupportedLanguage = Literal[
    "en",
    "fr",
    "pa",
    "hi",
    "es",
    "tl",
    "sw",
    "ti",
]


class IncomeSource(BaseModel):
    type: str
    amount: float = 0


class Dependent(BaseModel):
    relationship: str
    age: int


class AvatarProfile(BaseModel):
    skin_tone: str = "medium"
    hair_texture: str = "wavy"
    attire_style: str = "modern"
    accessories: list[str] = Field(default_factory=list)
    gesture_style: str = "wave"


class CulturalPreferences(BaseModel):
    culture_tags: list[str] = Field(default_factory=list)
    religion_tags: list[str] = Field(default_factory=list)
    celebration_theme: str = "global"
    preferred_address: str = "first_name"
    tone: Literal["formal", "informal", "kid_friendly"] = "formal"


class FamilyMember(BaseModel):
    member_id: str
    name: str
    role: str
    pronouns: str | None = None
    preferred_language: SupportedLanguage = "en"
    avatar: AvatarProfile = Field(default_factory=AvatarProfile)
    culture: CulturalPreferences = Field(default_factory=CulturalPreferences)


class TaxProfileCreate(BaseModel):
    user_id: str
    family_id: str
    member_id: str
    tax_year: str
    marital_status: str | None = None
    disability_status: str | None = None
    income_sources: list[IncomeSource] = Field(default_factory=list)
    dependents: list[Dependent] = Field(default_factory=list)
    financial_activity: list[str] = Field(default_factory=list)
    life_events: list[str] = Field(default_factory=list)
    localized_region: str = "CA"


class TaxProfileResponse(BaseModel):
    user_id: str
    family_id: str
    member_id: str
    tax_year: str
    income_sources: list[dict[str, Any]]
    dependents: list[dict[str, Any]]
    credits_eligibility: list[dict[str, Any]]
    deductions: list[dict[str, Any]]
    documents_uploaded: list[dict[str, Any]]
    memory_highlights: list[str]


class CreditSuggestion(BaseModel):
    name: str
    reason: str
    explainability: str


class CreditsReport(BaseModel):
    user_id: str
    tax_year: str
    potential_credits: list[CreditSuggestion]
    recurrent_deductions: list[str] = Field(default_factory=list)
    unused_credit_hints: list[str] = Field(default_factory=list)


class RiskReport(BaseModel):
    user_id: str
    tax_year: str
    risk_score: int
    warnings: list[str]
    explainability: list[str]
    cumulative_risk_trend: list[dict[str, Any]] = Field(default_factory=list)


class AccountantQuestions(BaseModel):
    user_id: str
    tax_year: str
    questions: list[str]


class ComplianceEventCreate(BaseModel):
    user_id: str
    family_id: str
    event: str
    details: dict[str, Any] = Field(default_factory=dict)


class ComplianceEventResponse(BaseModel):
    user_id: str
    family_id: str
    event: str
    details: dict[str, Any]


class FamilyHubCreate(BaseModel):
    family_id: str
    family_name: str
    preferred_language: SupportedLanguage = "en"
    family_structure: str = "nuclear"
    political_neutral_mode: bool = True
    members: list[FamilyMember] = Field(default_factory=list)


class GamificationProgress(BaseModel):
    family_id: str
    member_id: str
    points: int = 0
    level: int = 1
    streak_days: int = 0
    badges: list[str] = Field(default_factory=list)


class ConversationMemory(BaseModel):
    user_id: str
    tax_year: str
    question: str
    guidance: str


class LanguagePreferenceUpdate(BaseModel):
    family_id: str
    member_id: str
    preferred_language: SupportedLanguage




class IntegrationConnectionRequest(BaseModel):
    user_id: str
    family_id: str
    provider: str


class IntegrationConnection(BaseModel):
    connection_id: str
    user_id: str
    family_id: str
    provider: str
    status: Literal["pending", "connected", "revoked"] = "pending"
    oauth_url: str
    created_at: str


class SyncImportRequest(BaseModel):
    user_id: str
    provider: str
    tax_year: str


class SyncExportRequest(BaseModel):
    user_id: str
    provider: str
    tax_year: str
    approval: bool = False


class SyncEvent(BaseModel):
    user_id: str
    provider: str
    tax_year: str
    direction: Literal["import", "export"]
    status: str
    details: dict[str, Any] = Field(default_factory=dict)
class CulturePreferenceUpdate(BaseModel):
    family_id: str
    member_id: str
    culture: CulturalPreferences
    avatar: AvatarProfile


class CelebrationPacket(BaseModel):
    member_id: str
    language: SupportedLanguage
    animation_theme: str
    icon_set: list[str]
    localized_message: str
