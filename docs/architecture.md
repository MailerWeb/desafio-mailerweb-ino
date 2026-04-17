# Arquitetura do Sistema — Meeting Room Booking

Documento de referência da arquitetura adotada no projeto, cobrindo camadas de código, topologia de serviços, fluxos de dados e decisões estruturais.

---

## 1. Visão Geral

O sistema é uma aplicação fullstack de reservas de salas de reunião. O backend segue **Clean Architecture**, o frontend é uma SPA em React, e as notificações por e-mail são processadas de forma assíncrona via **Outbox Pattern + Celery Worker**.

```
┌──────────────────────────────────────────────────────┐
│                      Browser / SPA                   │
│                   React 18 + TypeScript               │
└─────────────────────────┬────────────────────────────┘
                          │ HTTP / JSON (JWT)
┌─────────────────────────▼────────────────────────────┐
│                    FastAPI Backend                    │
│     api/ → application/ → domain/ ← infrastructure/ │
└──────┬─────────────────────────────┬─────────────────┘
       │ asyncpg                     │ Redis (Celery broker)
┌──────▼──────┐              ┌───────▼───────┐
│ PostgreSQL  │              │  Celery Worker│
│   (dados)   │              │  (e-mails)    │
└──────┬──────┘              └───────┬───────┘
       │ outbox_events                │ SMTP
       └──────────────────────────────▼───────┐
                                     Mailpit  │
                                   (dev/test) │
                                              └─
```

---

## 2. Camadas do Backend (Clean Architecture)

```
backend/app/
├── domain/              ← Regras de negócio puras (sem framework)
│   ├── entities/        ← Dataclasses: User, Room, Booking, OutboxEvent
│   ├── exceptions.py    ← DomainError, OverlapError, InvalidDateError
│   └── validators.py    ← validate_booking_dates(), validate_duration()
│
├── application/         ← Casos de uso (orquestra domain + infra)
│   ├── interfaces/      ← ABCs dos repositórios (contratos)
│   ├── services/        ← AuthService, RoomService, BookingService
│   └── schemas/         ← DTOs Pydantic (request / response)
│
├── infrastructure/      ← Implementações concretas
│   ├── database/        ← SQLAlchemy models + sessão async
│   ├── repositories/    ← Implementações SQLAlchemy dos ABCs
│   ├── security/        ← JWT (python-jose) + bcrypt
│   └── email/           ← SMTP sender via aiosmtplib
│
├── api/                 ← Camada HTTP (FastAPI)
│   ├── routers/         ← Endpoints (auth, rooms, bookings)
│   └── dependencies.py  ← get_current_user, CurrentUser, get_db
│
└── worker/              ← Celery app + tasks (processamento de outbox)
```

### Regra de dependência

As setas de dependência apontam **para dentro**:

```
api/ ──→ application/ ──→ domain/
              │
infrastructure/ ──→ application/  (implementa interfaces)
```

O `domain/` não importa nada externo — é testável com pytest puro, sem banco de dados nem FastAPI.

---

## 3. Topologia de Serviços (Docker Compose)

| Serviço    | Imagem / Build              | Porta   | Função                                          |
|------------|-----------------------------|---------|-------------------------------------------------|
| `db`       | postgres:16                 | 5432    | Banco de dados principal                        |
| `redis`    | redis:7-alpine              | 6379    | Broker do Celery + cache de resultados          |
| `mailpit`  | axllent/mailpit             | 1025/8025 | SMTP local para dev (UI em :8025)             |
| `backend`  | compose/development/backend | 8000    | API FastAPI + Alembic migrations on startup     |
| `worker`   | compose/development/worker  | —       | Celery worker (processa outbox_events)          |
| `beat`     | compose/development/worker  | —       | Celery beat (agenda a task a cada 10s)          |
| `frontend` | compose/development/frontend| 5173    | Vite dev server (React SPA)                     |

### Dependências de inicialização

```
db ──→ backend ──→ worker
   └──→ redis  ──→ beat
mailpit ──→ worker
```

---

## 4. Modelo de Dados

```
users
  id (UUID PK)
  email (UNIQUE)
  name
  hashed_password
  role (OWNER | MEMBER)
  is_active
  created_at

rooms
  id (UUID PK)
  name (UNIQUE)
  capacity
  location
  description
  is_active
  created_at

bookings
  id (UUID PK)
  room_id (FK rooms)
  organizer_id (FK users)
  title
  start_at (timestamptz)
  end_at (timestamptz)
  status (active | canceled)
  created_at
  updated_at
  ── EXCLUDE USING gist (room_id WITH =, tstzrange(start_at, end_at) WITH &&)
     WHERE (status = 'active')   ← garante no-overlap no banco

booking_participants
  booking_id (FK bookings)
  user_id (FK users)
  ── PK composta (booking_id, user_id)

outbox_events
  id (UUID PK)
  event_type (BOOKING_CREATED | BOOKING_UPDATED | BOOKING_CANCELED)
  payload (JSONB)
  status (pending | processed | failed)
  idempotency_key (UUID UNIQUE)
  attempts
  max_attempts
  created_at
  processed_at
```

Diagrama completo em DBML: [`docs/schema.dbml`](./schema.dbml)

---

## 5. Fluxo: Criação de Reserva

```
POST /api/bookings
       │
       ▼
BookingService.create()
  1. validate_booking_dates()   ← domain/validators.py
  2. validate_duration()
  3. overlap_check query        ← app layer (retorna 409 amigável)
  ── BEGIN TRANSACTION ──────────────────────────────
  4. INSERT bookings
  5. INSERT outbox_events (BOOKING_CREATED, pending)
  ── COMMIT ─────────────────────────────────────────
       │
       ▼                        (assíncrono, ~10s depois)
Celery Beat agenda process_pending_events
       │
       ▼
OutboxRepository.get_pending()  ← SELECT FOR UPDATE SKIP LOCKED
       │
       ▼
SMTPSender.send()               ← aiosmtplib → Mailpit (dev) / SMTP real (prod)
       │
       ▼
outbox_event.status = 'processed'
```

**Por que a transação atômica importa:** se o INSERT no booking falhar, o evento de e-mail também é descartado (rollback). Impossível enviar notificação de uma reserva que não existe.

---

## 6. Fluxo: Autenticação

```
POST /api/auth/login  (OAuth2PasswordRequestForm)
       │
       ▼
AuthService.login()
  1. UserRepository.get_by_email()
  2. bcrypt.checkpw()           ← infrastructure/security/jwt.py
  3. create_access_token()      ← python-jose, HS256
       │
       ▼
{ access_token, token_type: "bearer" }

── Requisições autenticadas ──────────────────────────
GET /api/auth/me
  Authorization: Bearer <token>
       │
       ▼
get_current_user() dependency    ← api/dependencies.py
  1. decode_access_token()
  2. UserRepository.get_by_id()
  3. injeta User nas rotas protegidas
```

---

## 7. Prevenção de Conflitos de Reserva (3 camadas)

```
Requisição A               Requisição B (simultânea)
     │                           │
     ▼                           ▼
overlap_check query         overlap_check query
  (sem overlap ainda)         (sem overlap ainda, race!)
     │                           │
     ▼                           ▼
INSERT booking A            INSERT booking B
     │                           │
     ▼                           ▼
COMMIT ✓               EXCLUSION VIOLATION ✗
                        → asyncpg lança ExclusionViolationError
                        → handler converte em HTTP 409
```

Detalhes na [`docs/decisions.md`](./decisions.md#2-estratégia-de-concorrência-para-reservas).

---

## 8. Estratégia de Branches

```
main
├── feature-1-architecture-ci     ← infraestrutura + CI verde       ✓ merged
├── feature-2-domain-models       ← entidades + migrations           ✓ merged
├── feature-3-auth                ← autenticação + usuários          ✓ merged
├── feature-4-rooms               ← CRUD de salas
├── feature-5-bookings            ← reservas + overlap + concorrência
├── feature-6-outbox-worker       ← Outbox pattern + Celery worker
├── feature-7-frontend            ← React SPA
└── feature-8-polish              ← README, smoke test, CI 100%
```

Cada branch gera um PR com CI obrigatório verde antes de merge. Roadmap completo: [`docs/roadmap.md`](./roadmap.md)

---

## 9. Integração dos Apps Existentes

O projeto aproveitou três aplicações FastAPI internas, adaptando-as à clean architecture:

| App original       | O que foi aproveitado                              | Destino no projeto                                   |
|--------------------|----------------------------------------------------|------------------------------------------------------|
| `auth/security.py` | `create_access_token`, hash/verify senha           | `infrastructure/security/jwt.py`                     |
| `auth/current_user.py` | `get_current_user`, `CurrentUser` type alias   | `api/dependencies.py`                                |
| `auth/router.py`   | login (OAuth2), register, /me                      | `api/routers/auth.py` (simplificado)                 |
| `usuario/models.py`| estrutura User + role                              | `infrastructure/database/models.py` (UUID pk, sem tenant) |
| `usuario/services.py` | get_by_email, get_by_id, create              | `infrastructure/repositories/sqlalchemy_user_repo.py` |
| `tenant/services.py` | padrão `Service(session)` + `ServiceDep`       | todos os services do projeto                         |

**O que foi descartado:** 2FA (totp), rate_limit decorator, forgot/reset password, campos `tenant_id` e `llm_*`, multitenancy (não é requisito do desafio).

---

## 10. Estrutura de Testes

```
tests/
├── conftest.py          ← fixtures: engine, db_session, async_client, db_client
├── test_health.py       ← smoke test da API (CI mínimo)
├── unit/
│   ├── test_booking_validators.py
│   └── test_domain_rules.py
├── integration/
│   ├── test_auth_api.py
│   ├── test_rooms_api.py
│   ├── test_bookings_api.py
│   ├── test_booking_overlap.py
│   └── test_outbox_creation.py
└── worker/
    ├── test_outbox_processing.py
    └── test_idempotency.py
```

O banco de teste (`test_meetings`) é criado automaticamente no CI antes dos testes e usa a mesma migration do banco de produção.
