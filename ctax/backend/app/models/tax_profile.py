from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Text, func

from app.db.session import Base


class FamilyHub(Base):
    __tablename__ = "family_hubs"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(String(64), unique=True, index=True, nullable=False)
    family_name = Column(String(128), nullable=False)
    preferred_language = Column(String(8), nullable=False, default="en")
    family_structure = Column(String(64), nullable=False, default="nuclear")
    political_neutral_mode = Column(Boolean, nullable=False, default=True)
    members = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class TaxProfile(Base):
    __tablename__ = "tax_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), index=True, nullable=False)
    family_id = Column(String(64), index=True, nullable=False)
    member_id = Column(String(64), index=True, nullable=False)
    tax_year = Column(String(8), nullable=False)
    localized_region = Column(String(8), nullable=False, default="CA")
    marital_status = Column(String(32), nullable=True)
    disability_status = Column(String(32), nullable=True)
    income_sources = Column(JSON, nullable=False, default=list)
    dependents = Column(JSON, nullable=False, default=list)
    financial_activity = Column(JSON, nullable=False, default=list)
    life_events = Column(JSON, nullable=False, default=list)
    credits_eligibility = Column(JSON, nullable=False, default=list)
    deductions = Column(JSON, nullable=False, default=list)
    documents_uploaded = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class DocumentRecord(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), index=True, nullable=False)
    family_id = Column(String(64), index=True, nullable=False)
    member_id = Column(String(64), index=True, nullable=False)
    filename = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False)
    mime_type = Column(String(128), nullable=True)
    storage_path = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ConversationMemoryRecord(Base):
    __tablename__ = "conversation_memory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), index=True, nullable=False)
    tax_year = Column(String(8), nullable=False)
    question = Column(Text, nullable=False)
    guidance = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class GamificationProgressRecord(Base):
    __tablename__ = "gamification_progress"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(String(64), index=True, nullable=False)
    member_id = Column(String(64), index=True, nullable=False)
    points = Column(Integer, nullable=False, default=0)
    level = Column(Integer, nullable=False, default=1)
    streak_days = Column(Integer, nullable=False, default=0)
    badges = Column(JSON, nullable=False, default=list)
    cultural_theme = Column(String(64), nullable=False, default="global")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class ComplianceLog(Base):
    __tablename__ = "compliance_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), index=True, nullable=False)
    family_id = Column(String(64), index=True, nullable=False)
    event = Column(String(255), nullable=False)
    details = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class IntegrationConnectionRecord(Base):
    __tablename__ = "integration_connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), index=True, nullable=False)
    family_id = Column(String(64), index=True, nullable=False)
    provider = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False, default="pending")
    oauth_scope = Column(String(255), nullable=False, default="read_write_tax")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class SyncEventRecord(Base):
    __tablename__ = "sync_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), index=True, nullable=False)
    provider = Column(String(64), nullable=False)
    tax_year = Column(String(8), nullable=False)
    direction = Column(String(16), nullable=False)
    status = Column(String(32), nullable=False)
    details = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
