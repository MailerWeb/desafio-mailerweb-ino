# Decisões Técnicas

Registro das decisões de arquitetura e de biblioteca tomadas ao longo do projeto, com contexto e motivação.

---

## 1. Hashing de senhas: `bcrypt` direto em vez de `passlib` ou `pwdlib`

**Data:** 2026-04-17
**Status:** Adotado

### Contexto

O app de autenticação original (`auth/`) usava `pwdlib`, que é uma biblioteca de alto nível e serve como wrapper moderno sobre backends de hashing (bcrypt, argon2 etc.). Durante a portagem para este projeto, a dependência `passlib[bcrypt]` foi tentada primeiro por ser o backend mais comum em tutoriais FastAPI.

### Problema encontrado

`passlib` tem dois problemas no Python 3.12 / bcrypt 5.x:

1. O módulo `crypt` da stdlib foi removido no Python 3.13 e deprecado no 3.12 — passlib gera `DeprecationWarning` ao importar.
2. O `bcrypt 5.x` removeu o atributo `__about__` que o passlib usava para detectar a versão do backend, causando `AttributeError` silencioso e posterior `ValueError: password cannot be longer than 72 bytes` mesmo para senhas curtas.

### Decisão

Usar `bcrypt` diretamente, sem wrapper:

```python
import bcrypt

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
```

### Alternativas consideradas

| Biblioteca | Motivo de não usar |
|---|---|
| `passlib[bcrypt]` | Incompatível com bcrypt 5.x, deprecated no Python 3.12 |
| `pwdlib[bcrypt]` | Funciona, mas adiciona uma camada de abstração desnecessária para um único algoritmo |
| `argon2-cffi` | Mais seguro que bcrypt, mas fora do padrão de mercado para FastAPI e sem ganho real no contexto do desafio |

### Consequências

- API de hashing exposta em `app/infrastructure/security/jwt.py`
- Dependência `bcrypt>=4.0.0` no `pyproject.toml` (4.x e 5.x são compatíveis com nossa implementação)
- Limite de 72 bytes por senha é inerente ao algoritmo bcrypt — documentar no futuro se houver validação de tamanho máximo de senha

---

## 2. Estratégia de concorrência para reservas: Exclusion Constraint + validação em app

**Data:** 2026-04-17
**Status:** Adotado

### Contexto

O sistema precisa impedir que duas reservas ativas ocupem a mesma sala no mesmo horário, mesmo sob requisições concorrentes.

### Decisão

Três camadas de proteção:

1. **Validação na Application Layer** — query prévia para checar overlap antes de inserir (retorna erro amigável ao usuário).
2. **Exclusion Constraint no PostgreSQL** (`EXCLUDE USING gist`) — garante atomicidade no banco. Mesmo que duas requisições passem pela validação da app simultaneamente, o banco rejeita a segunda com `ExclusionViolationError`.
3. **Transação atômica** — `booking` + `outbox_event` são inseridos na mesma transação. Qualquer falha faz rollback completo.

```sql
ALTER TABLE bookings
ADD CONSTRAINT no_booking_overlap
EXCLUDE USING gist (
    room_id WITH =,
    tstzrange(start_at, end_at, '[)') WITH &&
) WHERE (status = 'active');
```

### Por que não só `SELECT FOR UPDATE`

`SELECT FOR UPDATE` serializa o acesso mas não garante atomicidade se a aplicação crashar entre o SELECT e o INSERT. A exclusion constraint age no nível do banco, independente do estado da aplicação.

---

## 3. Outbox Pattern para notificações por e-mail

**Data:** 2026-04-17
**Status:** Adotado

### Decisão

Ao criar/editar/cancelar uma reserva, o sistema persiste um evento na tabela `outbox_events` **na mesma transação** da operação de negócio. Um worker Celery processa esses eventos de forma assíncrona.

### Garantias

- **Consistência:** Se o INSERT do booking falhar, o evento não é criado (rollback atômico). Impossível enviar e-mail de uma reserva que não existe.
- **Idempotência:** Cada evento tem um `idempotency_key` UUID único com constraint `UNIQUE` no banco. O worker verifica o status antes de processar.
- **Resiliência:** `FOR UPDATE SKIP LOCKED` permite múltiplos workers sem duplicação. Retry automático com `attempts` e `max_attempts`.

---

## 4. Clean Architecture: separação domain / application / infrastructure

**Data:** 2026-04-17
**Status:** Adotado

### Estrutura

```
domain/          # Regras de negócio puras (sem framework)
  entities/      # Dataclasses: User, Room, Booking, OutboxEvent
  exceptions.py  # DomainError e subclasses
  validators.py  # Validações de data/duração

application/     # Casos de uso (orquestra domain + infrastructure)
  interfaces/    # ABCs dos repositórios
  services/      # AuthService, RoomService, BookingService
  schemas/       # DTOs Pydantic (request/response)

infrastructure/  # Implementações concretas
  database/      # SQLAlchemy models + session
  repositories/  # Implementações SQLAlchemy dos ABCs
  security/      # JWT + bcrypt
  email/         # SMTP sender (Fase 6)

api/             # Camada HTTP (FastAPI)
  routers/       # Endpoints
  dependencies.py # get_current_user, get_db
```

### Benefício principal

As regras de negócio (domain) não dependem de FastAPI, SQLAlchemy ou qualquer outro framework. São testáveis com pytest puro, sem banco de dados.
