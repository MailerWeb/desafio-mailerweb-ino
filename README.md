# Meeting Room Booking

Aplicação fullstack de reservas de salas com notificações assíncronas por e-mail.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2 async, asyncpg |
| Banco | PostgreSQL 16 (btree_gist + EXCLUDE USING gist) |
| Worker | Celery 5 + Redis |
| E-mail (dev) | Mailpit |
| Frontend | React 18 + TypeScript + Vite + Tailwind |
| Package manager | uv |
| Containers | Docker Compose |

---

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (para rodar testes e lint localmente)
- `make`

---

## Início rápido

```bash
git clone https://github.com/JuanLadeira/webchalleng.git
cd webchalleng

cp .env.example .env        # ajuste as variáveis se necessário
make up                     # sobe todos os 7 serviços
```

Aguarde os containers ficarem healthy e acesse:

| Serviço | URL |
|---|---|
| API | http://localhost:8000 |
| Documentação interativa | http://localhost:8000/docs |
| Frontend | http://localhost:5173 |
| Mailpit (e-mails dev) | http://localhost:8025 |

---

## Comandos disponíveis (`make`)

Todos os comandos são executados a partir da **raiz do projeto**.

### Containers

```bash
make up          # sobe todos os serviços em background
make down        # derruba todos os serviços
make rebuild     # rebuilda as imagens e sobe
make logs        # acompanha logs do backend em tempo real
```

### Banco de dados

```bash
make migrate     # aplica todas as migrations (alembic upgrade head)
make rollback    # reverte a última migration (alembic downgrade -1)
```

### Testes

```bash
make test        # roda todos os testes (precisa do banco rodando)
make test-cov    # testes com relatório de cobertura
make test-unit   # só testes unitários (sem banco)
make test-int    # só testes de integração
```

### Qualidade de código

```bash
make lint        # verifica erros de estilo com ruff
make fmt         # formata o código automaticamente
make fmt-check   # checa formatação sem alterar arquivos
```

### Outros

```bash
make install     # instala dependências de dev (uv sync --extra dev)
make help        # lista todos os comandos com descrição
```

---

## Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste conforme necessário.

| Variável | Padrão | Descrição |
|---|---|---|
| `POSTGRES_USER` | `user` | Usuário do banco |
| `POSTGRES_PASSWORD` | `pass` | Senha do banco |
| `POSTGRES_DB` | `meetings` | Nome do banco |
| `POSTGRES_HOST` | `db` | Host do banco (`localhost` fora do Docker) |
| `POSTGRES_PORT` | `5432` | Porta do banco |
| `REDIS_HOST` | `redis` | Host do Redis (`localhost` fora do Docker) |
| `REDIS_PORT` | `6379` | Porta do Redis |
| `JWT_SECRET_KEY` | `change-me` | Chave secreta para assinar tokens JWT |
| `JWT_ALGORITHM` | `HS256` | Algoritmo JWT |
| `JWT_EXPIRATION_MINUTES` | `60` | Validade do token em minutos |
| `SMTP_HOST` | `mailpit` | Host SMTP |
| `SMTP_PORT` | `1025` | Porta SMTP |
| `SMTP_FROM` | `noreply@...` | Remetente dos e-mails |
| `SMTP_TLS` | `false` | TLS no SMTP (true em produção) |
| `OUTBOX_POLL_INTERVAL_SECONDS` | `10` | Intervalo do worker de outbox |

---

## Arquitetura

O backend segue **Clean Architecture** com 4 camadas:

```
domain/          ← regras de negócio puras (sem framework)
application/     ← casos de uso + interfaces dos repositórios
infrastructure/  ← SQLAlchemy, bcrypt, SMTP, Celery
api/             ← routers FastAPI + dependencies
```

A regra central: dependências sempre apontam para dentro. O `domain/` não importa nada externo e é testável com pytest puro.

Documentação detalhada:

- [`docs/architecture.md`](docs/architecture.md) — visão geral, fluxos e topologia de serviços
- [`docs/clean-architecture.md`](docs/clean-architecture.md) — comparação com MVC, Hexagonal e DDD
- [`docs/decisions.md`](docs/decisions.md) — decisões técnicas (bcrypt, overlap constraint, outbox)
- [`docs/schema.dbml`](docs/schema.dbml) — diagrama do banco (dbdiagram.io)

---

## Serviços Docker

| Serviço | Imagem | Porta | Função |
|---|---|---|---|
| `db` | postgres:16 | 5432 | Banco principal |
| `redis` | redis:7-alpine | 6379 | Broker Celery |
| `mailpit` | axllent/mailpit | 1025 / 8025 | SMTP dev + UI |
| `backend` | build local | 8000 | API FastAPI |
| `worker` | build local | — | Celery worker (outbox) |
| `beat` | build local | — | Celery beat (scheduler) |
| `frontend` | build local | 5173 | React SPA |

---

## Endpoints da API

A documentação completa está em http://localhost:8000/docs (Swagger UI).

### Autenticação

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/auth/register` | Cria novo usuário |
| `POST` | `/api/auth/login` | Login — retorna JWT |
| `GET` | `/api/auth/me` | Dados do usuário autenticado |

### Salas

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/rooms` | Cria sala |
| `GET` | `/api/rooms` | Lista salas ativas |
| `GET` | `/api/rooms/{id}` | Detalhe da sala |
| `PATCH` | `/api/rooms/{id}` | Atualiza sala |
| `DELETE` | `/api/rooms/{id}` | Desativa sala (soft delete) |

### Reservas _(em desenvolvimento — Fase 5)_

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/bookings` | Cria reserva |
| `GET` | `/api/bookings` | Lista reservas do usuário |
| `GET` | `/api/bookings/{id}` | Detalhe da reserva |
| `PATCH` | `/api/bookings/{id}` | Atualiza reserva |
| `DELETE` | `/api/bookings/{id}` | Cancela reserva |

---

## Prevenção de conflito de reservas

Três camadas de proteção:

1. **Validação na application layer** — query de overlap antes de inserir, retorna HTTP 409 com mensagem amigável
2. **EXCLUDE USING gist no PostgreSQL** — garante atomicidade mesmo sob requisições concorrentes
3. **Transação atômica** — `booking` + `outbox_event` inseridos juntos; qualquer falha faz rollback completo

```sql
EXCLUDE USING gist (
    room_id WITH =,
    tstzrange(start_at, end_at, '[)') WITH &&
) WHERE (status = 'active')
```

---

## Notificações por e-mail (Outbox Pattern)

1. Ao criar/editar/cancelar uma reserva, um evento é persistido em `outbox_events` **na mesma transação**
2. O Celery Beat dispara `process_pending_events` a cada 10 segundos
3. O worker busca eventos com `SELECT FOR UPDATE SKIP LOCKED` (suporte a múltiplos workers sem duplicação)
4. Cada evento tem `idempotency_key` UUID único — reprocessamentos são ignorados

Em desenvolvimento, os e-mails são capturados pelo **Mailpit** em http://localhost:8025.

---

## Testes

```
tests/
├── unit/               ← domain puro, sem banco (rápido)
├── integration/        ← API completa com banco de teste
└── worker/             ← outbox processing + idempotência
```

O banco de testes (`test_meetings`) é criado automaticamente no CI. Localmente, basta ter o Docker rodando e executar `make test`.

CI no GitHub Actions: `.github/workflows/backend-tests.yml` — roda a cada push com postgres e redis como services.

---

## Progresso do desenvolvimento

| Fase | Branch | Status |
|---|---|---|
| 1 — Infraestrutura + CI | `feature-1-architecture-ci` | Concluída |
| 2 — Domain + Models | `feature-2-domain-models` | Concluída |
| 3 — Autenticação | `feature-3-auth` | Concluída |
| 4 — Salas | `feature-4-rooms` | Em andamento |
| 5 — Reservas | `feature-5-bookings` | Pendente |
| 6 — Outbox + Worker | `feature-6-outbox-worker` | Pendente |
| 7 — Frontend | `feature-7-frontend` | Pendente |
| 8 — Polish + Docs | `feature-8-polish` | Pendente |
