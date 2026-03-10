
## Como rodar o Backend

1. Instale as dependências:
   ```bash
   cd backend
   uv sync
   ```
2. Configure as variáveis de ambiente:
   ```bash
   cp ../.env.example ../.env
   ```
3. Rode as migrações:
   ```bash
   uv run alembic upgrade head
   ```
4. Inicie a API:
   ```bash
   uv run uvicorn main:app --reload
   ```

## Como rodar o Worker

Em outro terminal:
```bash
uv run celery -A celery_app worker --loglevel=info
```

## Como rodar o Frontend

1. Instale as dependências:
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   ```
2. Inicie o frontend:
   ```bash
   npm run dev
   ```
3. Rode os testes:
   ```bash
   npm run test
   ```

## Variáveis de Ambiente

Veja o arquivo `.env.example` para todas as variáveis necessárias:

- DB_USER
- DB_PASSWORD
- DB_DATABASE
- DB_PORT
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES
- CELERY_BROKER_URL
- CELERY_RESULT_BACKEND
- SMTP_SERVER
- SMTP_PORT
- SMTP_USER
- SMTP_PASSWORD
- EMAIL_FROM
- AMBIENTE_ATUAL
- PORT
- HOST

## Decisões Técnicas

- Backend: FastAPI + SQLAlchemy + Celery + Redis
  - Transações para prevenir overlaps
  - Padrão Outbox para notificações assíncronas
  - JWT para autenticação
- Frontend: React + Vite + Axios
  - Validação client-side
  - Loading states e tratamento de erros
  - Responsivo

---

Para rodar tudo com Docker Compose:

```bash
cp .env.example .env
docker-compose up -d
docker-compose exec app uv run alembic upgrade head
```

Acesse:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
