# Shopify AI Helpdesk (Gorgias-style)

Production-oriented full-stack helpdesk for Shopify brands.

## Monorepo Structure

- `backend/` FastAPI + MongoDB (Motor) + JWT + Mailgun webhooks + OpenAI AI replies
- `frontend/` React (Vite) + Tailwind + Axios + React Router

## Backend Structure

```txt
backend/app/
  core/
  db/
  middleware/
  models/
  routers/
  schemas/
  services/
```

### Collections

- `tickets`
- `messages`
- `customers`
- `agents`
- `automation_rules`
- `activity_logs`

## API Endpoints

### Auth
- `POST /auth/login`
- `GET /auth/me`

### Tickets
- `GET /tickets`
- `POST /tickets`
- `GET /tickets/{id}`
- `PATCH /tickets/{id}`

### Messages
- `GET /tickets/{id}/messages`
- `POST /tickets/{id}/messages`

### AI
- `POST /ai/suggest-reply/{ticket_id}`

### Shopify
- `GET /customers/{email}/profile`

### Webhooks
- `POST /webhooks/orders/create`
- `POST /webhooks/customers/update`
- `POST /webhooks/email/inbound`

## Environment Variables

Backend (`backend/.env` from `.env.example`):

- `MONGO_URI`
- `MONGO_DB_NAME`
- `JWT_SECRET`
- `JWT_ALGORITHM`
- `JWT_EXP_MINUTES`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `SHOPIFY_STORE_DOMAIN`
- `SHOPIFY_ADMIN_TOKEN`
- `SHOPIFY_WEBHOOK_SECRET`
- `MAILGUN_SIGNING_KEY`

Frontend (`frontend/.env` from `.env.example`):

- `VITE_API_BASE_URL`

## Local Setup

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts_seed.py
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Core Flow

`Email -> Ticket -> Message -> AI Suggestion -> Agent Dashboard`

## Deployment Notes

### Dev (Render)
- Deploy backend as a Render Web Service (`uvicorn app.main:app --host 0.0.0.0 --port $PORT`).
- Attach managed MongoDB or external MongoDB URI.
- Deploy frontend as Static Site with `npm run build` and publish `dist`.

### Prod (DigitalOcean)
- Host backend in App Platform or Droplet with process manager.
- Use DigitalOcean Managed MongoDB.
- Store secrets in DO environment manager.
- Place frontend behind CDN and HTTPS.
