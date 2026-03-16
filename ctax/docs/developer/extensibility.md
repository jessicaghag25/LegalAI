# CTax Developer Extensibility Guide (Inclusivity + Integrations)

## Add a New Tax Software Provider

1. Add provider key/name in `backend/app/services/integration_engine.py::SUPPORTED_PROVIDERS`.
2. Add any provider-specific mapping rules in import/export helpers.
3. Keep OAuth scope minimal (`read_write_tax` or narrower if possible).
4. Log all connection and sync events for auditability.

## Add Import Mapping Rules

1. Extend `import_snapshot()` transformation logic.
2. Map external forms to CTax objects (`income_sources`, `documents`, `credits`, `risk_alerts`).
3. Add explainability notes for transformed fields.

## Add Export Formats

1. Extend `export_package()` format list and serializers.
2. Require explicit user approval before export endpoint succeeds.
3. Preserve PII minimization and encryption assumptions.

## Add a New Language / Dialect

1. Add locale JSON at `ctax/frontend/src/locales/<lang>/translation.json`.
2. Register in `Dashboard.jsx` dictionary.
3. Add language/dialect hints in `backend/app/services/i18n.py`.

## Compliance Guardrails

- Always include multilingual disclaimer.
- No legal filing decisions or automatic filing.
- No political messaging.
- Respect cultural/religious boundaries and user identity preferences.
