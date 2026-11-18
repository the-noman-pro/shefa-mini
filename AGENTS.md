# Shefa mini: working notes

## Stack
- `backend/`: Python 3.12, Django 5.2 LTS, Django REST Framework (token auth), whitenoise, gunicorn, psycopg 3.
  SQLite by default, Postgres when `DATABASE_URL` is set. Pinned in `requirements.txt` (runtime) and
  `requirements-dev.txt` (adds ruff, pytest, pytest-django).
- `frontend/`: Vue 3 (`<script setup>`, plain JS), Vite 7, Vue Router 4, Pinia. ESLint 10 (flat config) + Prettier.
  Vitest 4 with jsdom. Fonts are bundled from `@fontsource-variable` (Fraunces, Instrument Sans): no CDN calls.

## Commands
Backend, from `backend/` with the venv active:
- `python manage.py runserver 8000` · `python manage.py migrate` · `python manage.py seed_cases [--demo-user]`
- `ruff check .` · `ruff format .` · `pytest` · `python manage.py check --deploy` (with DEBUG off)
- Production-style: `python manage.py collectstatic --noinput` then `gunicorn config.wsgi:application -b 0.0.0.0:8000`

Frontend, from `frontend/`:
- `npm run dev` (5173) · `npm run build` (to `dist/`) · `npm run preview` (4173)
- `npm run lint` · `npm run format` · `npm run format:check` · `npm run test`

## Layout
```
backend/
  config/            settings (all from env), urls, wsgi
  apps/core/         health check, reference generator
  apps/accounts/     custom User (email login, name), signup/login/logout/me
  apps/wallets/      Wallet + Transaction ledger, cards.py (Luhn/brand/expiry/CVV), top-up service
  apps/cases/        Case + Donation, donate service (atomic, select_for_update), seed_cases command
  tests/             empty: tests go here
  conftest.py        pytest treats "no tests collected" as a pass; delete that hook once tests exist
frontend/
  src/lib/           api.js (fetch wrapper, ApiError), card.js (same card rules as the server), money.js
  src/stores/        auth.js (token in localStorage, user, balance)
  src/views/         Cases, CaseDetail, DonationSuccess, Account, TopUp, Login, Signup, NotFound
  src/components/    ProgressJar, CardPreview, Money, Icon, CaseCard, Celebration, art/ (hand-drawn SVGs)
  src/styles/        tokens.css (colour/type/spacing custom properties), base.css
  tests/             empty: tests go here (vitest picks up tests/**/*.test.js)
```

## Environment variables
Backend (`backend/.env.example`; a `backend/.env` is read when present, real env vars win):

| Name | Default | Notes |
|---|---|---|
| `SECRET_KEY` | none | Required when `DEBUG` is off; startup fails without it |
| `DEBUG` | `false` | `true` for local work only |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma separated |
| `DATABASE_URL` | SQLite `backend/db.sqlite3` | e.g. `postgres://shefa:shefa@db:5432/shefa`; empty counts as unset |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Origins of the Vue app |
| `CSRF_TRUSTED_ORIGINS` | empty | Needed for the admin when served behind another origin/HTTPS |
| `USE_X_FORWARDED_PROTO` | `false` | Trust `X-Forwarded-Proto` from a TLS-terminating proxy |
| `SECURE_COOKIES` | `false` | Secure session/CSRF cookies (HTTPS only) |
| `DB_CONN_MAX_AGE` | `60` | Seconds to keep DB connections |
| `LOG_LEVEL` | `INFO` | Logs go to stdout |
| `AUTH_THROTTLE_RATE` / `TOP_UP_THROTTLE_RATE` | `30/min` / `20/min` | Per-client limits |

Frontend (`frontend/.env.example`):

| Name | Notes |
|---|---|
| `VITE_API_URL` | API base, no trailing slash. **Baked in at build time.** Empty = same origin (`/api/...`, behind a proxy) |

## API (all under `/api/`, JSON, `Authorization: Token <key>` where marked)
| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `health/` | no | `{"status":"ok","db":"ok"}`, 503 when the DB is down |
| POST | `auth/signup/` | no | `{name,email,password}` → `{token,user}` (201) |
| POST | `auth/login/` | no | `{email,password}` → `{token,user}` |
| POST | `auth/logout/` | yes | deletes the token (204) |
| GET/PATCH | `auth/me/` | yes | profile + wallet balance; PATCH `{name}` |
| GET | `wallet/` | yes | `{balance,currency,updated_at}` |
| GET | `wallet/transactions/?page=` | yes | ledger, newest first, 20 per page |
| POST | `wallet/top-up/` | yes | `{card_holder,card_number,expiry,cvv,amount}` → 201 approved, 402 declined, 400 field errors |
| GET | `cases/?category=&status=` | no | all cases, open first |
| GET | `cases/summary/` | no | totals + categories with counts |
| GET | `cases/<slug>/` | no | case + story + 8 recent donations |
| POST | `cases/<slug>/donate/` | yes | `{amount,anonymous}` → receipt (201); 400 when funded, below 10, over remaining or over balance (`code: insufficient_balance`) |
| GET | `donations/<reference>/` | yes | the caller's own receipt |

## Rules that matter
- Money is `Decimal` with 2 places end to end; the API sends amounts as strings.
- Card number and CVV are validated and dropped. Only brand + last 4 are stored; request bodies are never logged.
- Test card `4000 0000 0000 0002` is always declined; any other valid card is approved.
- Donations lock the wallet and the case row (`select_for_update`) inside `transaction.atomic`.
- Card rules exist twice (`backend/apps/wallets/cards.py`, `frontend/src/lib/card.js`); change both together.
