# Booking System Backend

## Setup Local

1. Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Install dependencies: `uv sync`
3. Set up environment variables in `.env`
4. Run database migrations (if any)
5. Start the API: `uv run uvicorn main:app --reload`
6. Start the worker: `uv run celery -A celery_app worker --loglevel=info`

## Setup com Docker

### Pré-requisitos
- Docker
- Docker Compose

### Iniciar a aplicação

1. Copiar o `.env.example` para `.env` e ajustar variáveis:
```bash
cp .env.example .env
```

2. Iniciar todos os serviços:
```bash
docker-compose up -d
```

3. Executar migrações de banco (se necessário):
```bash
docker-compose exec app uv run alembic upgrade head
```

### Serviços

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### Parar a aplicação

```bash
docker-compose down
```

### Ver logs

```bash
# API
docker-compose logs -f app

# Worker
docker-compose logs -f worker

# Database
docker-compose logs -f postgres
```

## Concurrency Strategy

To prevent concurrent bookings from overlapping, we use database transactions. Before creating or updating a booking, we check for overlaps within the same transaction. If an overlap is found, the transaction is rolled back.

## Worker Execution

The worker processes outbox events asynchronously using Celery with Redis as broker.

### Local Worker
```bash
uv run celery -A celery_app worker --loglevel=info
```

### Docker Worker
The worker runs automatically in the docker-compose setup as a separate service.

For periodic processing, configure Celery Beat or use a cron job to call the `/outbox/process` endpoint.