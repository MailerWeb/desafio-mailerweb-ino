.PHONY: help up down logs build clean dev docker-up docker-down migrations

help:
	@echo "Booking System - Comandos disponíveis:"
	@echo ""
	@echo "=== Docker (Produção) ==="
	@echo "  make docker-up           Iniciar containers (produção)"
	@echo "  make docker-down         Parar containers"
	@echo "  make docker-logs         Ver logs dos containers"
	@echo "  make docker-clean        Remover containers e volumes"
	@echo "  make docker-reset        Reset completo (rebuilda tudo)"
	@echo ""
	@echo "=== Desenvolvimento Local ==="
	@echo "  make dev                 Iniciar ambiente de desenvolvimento"
	@echo "  make dev-api             Iniciar API apenas"
	@echo "  make dev-worker          Iniciar Worker apenas"
	@echo "  make dev-postgres        Iniciar PostgreSQL"
	@echo "  make dev-redis           Iniciar Redis"
	@echo ""
	@echo "=== Database ==="
	@echo "  make migrations          Criar e aplicar migrations"
	@echo "  make migrate-up          Aplicar últimas migrations"
	@echo "  make migrate-down        Reverter última migration"
	@echo "  make backup              Fazer backup do banco"
	@echo ""
	@echo "=== Utils ==="
	@echo "  make shell-app           Acessar shell do container app"
	@echo "  make shell-worker        Acessar shell do container worker"
	@echo "  make shell-postgres      Acessar shell do PostgreSQL"
	@echo "  make shell-redis         Acessar Redis CLI"
	@echo ""

# Docker targets
docker-up:
	@echo "Iniciando containers..."
	@docker-compose up -d
	@echo "Containers iniciados!"
	@echo "API: http://localhost:8000/docs"

docker-down:
	@echo "Parando containers..."
	@docker-compose down
	@echo "Containers parados!"

docker-logs:
	@docker-compose logs -f

docker-clean:
	@echo "Limpando containers..."
	@docker-compose down -v
	@echo "Containers e volumes removidos!"

docker-reset:
	@echo "Fazendo reset completo..."
	@docker-compose down -v
	@docker-compose build --no-cache
	@docker-compose up -d
	@echo "Reset concluído!"

docker-prod-up:
	@echo "Iniciando produção..."
	@docker-compose -f docker-compose.prod.yml up -d
	@echo "Produção iniciada!"

docker-prod-down:
	@echo "Parando produção..."
	@docker-compose -f docker-compose.prod.yml down
	@echo "Produção parada!"

# Development targets
dev:
	@./run_dev.sh

dev-api:
	@./run_dev.sh api

dev-worker:
	@./run_dev.sh worker

dev-postgres:
	@./run_dev.sh postgres

dev-redis:
	@./run_dev.sh redis

# Database targets
migrations:
	@docker-compose exec app uv run alembic revision --autogenerate
	@docker-compose exec app uv run alembic upgrade head

migrate-up:
	@echo "Aplicando migrations..."
	@docker-compose exec app uv run alembic upgrade head
	@echo "Migrations aplicadas!"

migrate-down:
	@echo "Revertendo última migration..."
	@docker-compose exec app uv run alembic downgrade -1
	@echo "Migration revertida!"

backup:
	@echo "Fazendo backup do banco..."
	@mkdir -p backups
	@docker-compose exec -T postgres pg_dump -U $(DB_USER) $(DB_DATABASE) > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup realizado!"

# Shell targets
shell-app:
	@docker-compose exec app bash

shell-worker:
	@docker-compose exec worker bash

shell-postgres:
	@docker-compose exec postgres psql -U $(DB_USER) -d $(DB_DATABASE)

shell-redis:
	@docker-compose exec redis redis-cli

# Misc targets
install:
	@cd backend && uv sync

test:
	@docker-compose exec app uv run pytest

lint:
	@docker-compose exec app uv run ruff check backend

format:
	@docker-compose exec app uv run ruff format backend

ps:
	@docker-compose ps

build:
	@docker-compose build

rebuild:
	@docker-compose build --no-cache
