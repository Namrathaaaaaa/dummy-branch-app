# Flask Microloans API + Postgres (Docker)

Minimal REST API for microloans, built with Flask, SQLAlchemy, Alembic, and PostgreSQL (via Docker Compose).

## Quick start

```bash
# 1) Build and start services
docker compose up -d --build

# 2) Run DB migrations
docker compose exec api alembic upgrade head

# 3) Seed dummy data (idempotent)
docker compose exec api python scripts/seed.py

# 4) Hit endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/loans
```

## Configuration

See `.env.example` for env vars. By default:
- `DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/microloans`
- API listens on `localhost:8000`.

## API

- GET `/health` → `{ "status": "ok" }`
- GET `/api/loans` → list all loans
- GET `/api/loans/:id` → get loan by id
- POST `/api/loans` → create loan (status defaults to `pending`)

Example create:
```bash
curl -X POST http://localhost:8000/api/loans \
  -H 'Content-Type: application/json' \
  -d '{
    "borrower_id": "usr_india_999",
    "amount": 12000.50,
    "currency": "INR",
    "term_months": 6,
    "interest_rate_apr": 24.0
  }'
```

- GET `/api/stats` → aggregate stats: totals, avg, grouped by status/currency.

## Development

- App entrypoint: `wsgi.py` (`wsgi:app`)
- Flask app factory: `app/__init__.py`
- Models: `app/models.py`
- Migrations: `alembic/`

## Notes

- Amounts are validated server-side (0 < amount ≤ 50000).
- No authentication for this prototype.