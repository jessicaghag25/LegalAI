# CTax 3.3 – Inclusive Multilingual Family Tax Adventure Assistant

CTax 3.3 is a memory-driven, gamified, multilingual tax preparation diagnostic platform for diverse families and identities.

> **Disclaimer:** CTax provides educational guidance and is not a substitute for professional tax advice.

## Core Experience

- 👨‍👩‍👧‍👦 Family Hub with flexible roles and inclusive profiles
- 🧠 Cumulative memory across years (deductions, risks, Q&A history)
- 🎮 Gamification with points, badges, streaks, mini-games, and adventure map
- 🌍 Multilingual UX + dialect hints (EN, FR, PA, HI, ES, TL, SW, TI)
- 🎨 Cultural inclusivity features with avatar and celebration customization
- ⚠️ CT Scan risk engine + explainable risk trend
- 🧾 Compliance log for good-faith preparation trail

## Tax Software Integration Hub

CTax now includes a software integration layer to connect external filing tools while preserving user consent and compliance:

- CRA My Account / NETFILE-compatible tools
- TurboTax / TurboTax Online
- BetterTax
- H&R Block / UFile

Capabilities:
- OAuth-based connection scaffolding
- Import snapshots of prior-year data, deductions, credits, and risk hints
- Export package generation with explicit user approval gate
- Sync history and reminders for filing deadlines
- Family dashboard + gamification continuity after import

## Integration Endpoints

- `GET /api/v1/integrations/providers`
- `POST /api/v1/integrations/connect`
- `POST /api/v1/integrations/sync/import`
- `POST /api/v1/integrations/sync/export`
- `GET /api/v1/integrations/sync/{user_id}`
- `GET /api/v1/integrations/reminders/{user_id}`

## Run Backend

```bash
cd ctax/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run Frontend

```bash
cd ctax/frontend
npm install
npm run dev
```
