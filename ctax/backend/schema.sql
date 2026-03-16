CREATE TABLE family_hubs (
  id SERIAL PRIMARY KEY,
  family_id VARCHAR(64) UNIQUE NOT NULL,
  family_name VARCHAR(128) NOT NULL,
  preferred_language VARCHAR(8) NOT NULL DEFAULT 'en',
  family_structure VARCHAR(64) NOT NULL DEFAULT 'nuclear',
  political_neutral_mode BOOLEAN NOT NULL DEFAULT TRUE,
  members JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE tax_profiles (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  family_id VARCHAR(64) NOT NULL,
  member_id VARCHAR(64) NOT NULL,
  tax_year VARCHAR(8) NOT NULL,
  localized_region VARCHAR(8) NOT NULL DEFAULT 'CA',
  marital_status VARCHAR(32),
  disability_status VARCHAR(32),
  income_sources JSONB NOT NULL DEFAULT '[]'::jsonb,
  dependents JSONB NOT NULL DEFAULT '[]'::jsonb,
  financial_activity JSONB NOT NULL DEFAULT '[]'::jsonb,
  life_events JSONB NOT NULL DEFAULT '[]'::jsonb,
  credits_eligibility JSONB NOT NULL DEFAULT '[]'::jsonb,
  deductions JSONB NOT NULL DEFAULT '[]'::jsonb,
  documents_uploaded JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  family_id VARCHAR(64) NOT NULL,
  member_id VARCHAR(64) NOT NULL,
  filename VARCHAR(255) NOT NULL,
  category VARCHAR(64) NOT NULL,
  mime_type VARCHAR(128),
  storage_path TEXT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE conversation_memory (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  tax_year VARCHAR(8) NOT NULL,
  question TEXT NOT NULL,
  guidance TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE gamification_progress (
  id SERIAL PRIMARY KEY,
  family_id VARCHAR(64) NOT NULL,
  member_id VARCHAR(64) NOT NULL,
  points INTEGER NOT NULL DEFAULT 0,
  level INTEGER NOT NULL DEFAULT 1,
  streak_days INTEGER NOT NULL DEFAULT 0,
  badges JSONB NOT NULL DEFAULT '[]'::jsonb,
  cultural_theme VARCHAR(64) NOT NULL DEFAULT 'global',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE integration_connections (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  family_id VARCHAR(64) NOT NULL,
  provider VARCHAR(64) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'pending',
  oauth_scope VARCHAR(255) NOT NULL DEFAULT 'read_write_tax',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE sync_events (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  provider VARCHAR(64) NOT NULL,
  tax_year VARCHAR(8) NOT NULL,
  direction VARCHAR(16) NOT NULL,
  status VARCHAR(32) NOT NULL,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE compliance_logs (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  family_id VARCHAR(64) NOT NULL,
  event VARCHAR(255) NOT NULL,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_family_hubs_family_id ON family_hubs(family_id);
CREATE INDEX idx_tax_profiles_user_year ON tax_profiles(user_id, tax_year);
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_memory_user_id ON conversation_memory(user_id);
CREATE INDEX idx_gamification_family_id ON gamification_progress(family_id);
CREATE INDEX idx_integrations_user_id ON integration_connections(user_id);
CREATE INDEX idx_sync_events_user_id ON sync_events(user_id);
CREATE INDEX idx_compliance_logs_user_id ON compliance_logs(user_id);
