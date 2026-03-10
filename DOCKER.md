# Docker Setup Guide

## Estrutura

O projeto usa Docker Compose com 3 serviços:
- **PostgreSQL**: Banco de dados
- **Redis**: Broker para Celery
- **App**: API FastAPI + Worker Celery

## Pré-requisitos

Ter instalado:
- Docker
- Docker Compose

## Configuração

### 1. Criar arquivo `.env`

```bash
cp .env.example .env
```

Editar `.env` com as credenciais corretas:

```env
# Database
DB_USER=postgres
DB_PASSWORD=sua_senha_segura
DB_DATABASE=booking_db

# Authentication
SECRET_KEY=uma_chave_super_secreta_e_longa

# Email (Gmail)
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-de-app
```

### 2. Iniciar serviços

```bash
# Iniciar em background
docker-compose up -d

# Ou Ver logs em tempo real
docker-compose up
```

### 3. Verificar saúde dos serviços

```bash
docker-compose ps
```

Esperar todos os serviços ficarem `healthy`.

### 4. Executar migrações

```bash
docker-compose exec app uv run alembic upgrade head
```

## Uso

### Acessar a API

- **Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Ver logs

```bash
# Todos
docker-compose logs -f

# API apenas
docker-compose logs -f app

# Worker apenas
docker-compose logs -f worker

# Database
docker-compose logs -f postgres

# Redis
docker-compose logs -f redis
```

### Executar comandos no container

```bash
# Dentro da app
docker-compose exec app uv run python -c "print('test')"

# Dentro do worker
docker-compose exec worker uv run celery -A celery_app inspect active
```

### Reset completo

```bash
# Parar e remover tudo
docker-compose down -v

# Reconstruir imagens
docker-compose build --no-cache

# Iniciar novamente
docker-compose up -d
```

## Database

### Acessar o PostgreSQL

```bash
docker-compose exec postgres psql -U postgres -d booking_db
```

### Backup

```bash
docker-compose exec postgres pg_dump -U postgres booking_db > backup.sql
```

### Restore

```bash
docker-compose exec -T postgres psql -U postgres booking_db < backup.sql
```

## Redis

### Acessar o Redis CLI

```bash
docker-compose exec redis redis-cli
```

### Limpar cache

```bash
docker-compose exec redis redis-cli FLUSHALL
```

## Troubleshooting

### Porta já em uso

Se uma porta estiver em uso, editar `docker-compose.yml`:

```yaml
postgres:
  ports:
    - "5433:5432"  # Mudar porta externa
```

### Permissões do volume

```bash
docker-compose exec app chmod -R 755 /app
```

### Rebuild necessário

```bash
docker-compose build --no-cache app worker
docker-compose up -d
```

## Environment Variables

Ver `.env.example` para todas as variáveis disponíveis.

### Variáveis críticas

- `SECRET_KEY`: Mudar em produção
- `SMTP_USER` e `SMTP_PASSWORD`: Configurar para enviar emails
- `DB_PASSWORD`: Mudar em produção
