# Shefa mini

A small donation app: sign up, top up a wallet with a (dummy) card, give to a charity case, get a receipt.
Django REST API in `backend/`, Vue 3 app in `frontend/`. Amounts are in SAR. No real money moves anywhere:
the card processor is simulated.

## Run it locally

Needs Python 3.12 and Node 20.19+.

```bash
# API on http://localhost:8000
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env              # DEBUG=true locally; set SECRET_KEY anywhere else
python manage.py migrate
python manage.py seed_cases --demo-user
python manage.py runserver 8000
```

```bash
# Web app on http://localhost:5173
cd frontend
cp .env.example .env.local        # VITE_API_URL=http://localhost:8000
npm install
npm run dev
```

Demo login: `demo@shefa-mini.test` / `GiveWell2026` (wallet starts at 500 SAR).
Django admin: `python manage.py createsuperuser`, then http://localhost:8000/admin/.

Test cards: `4242 4242 4242 4242` is approved, `4000 0000 0000 0002` is always declined. Any expiry in the future,
any 3-digit code.

## Checks

| | Backend (`backend/`) | Frontend (`frontend/`) |
|---|---|---|
| Lint | `ruff check .` and `ruff format --check .` | `npm run lint` and `npm run format:check` |
| Tests | `pytest` | `npm run test` |
| Build | `python manage.py check` | `npm run build` |

## Health

`GET /api/health/` answers `{"status": "ok", "db": "ok"}` after a real query against the database, or 503 when the
database is unreachable.

More detail (layout, env vars, API) is in [AGENTS.md](AGENTS.md).
