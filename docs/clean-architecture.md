# Clean Architecture — Conceito e Comparações

---

## O que é

Clean Architecture é um modelo de organização de código criado por Robert Martin (Uncle Bob). O objetivo central é garantir que **as regras de negócio não dependam de tecnologia** — framework, banco de dados, protocolo HTTP ou qualquer detalhe de infraestrutura.

A consequência prática: você pode trocar o banco, o framework web ou o protocolo de entrega sem tocar nas regras de negócio.

---

## A regra de dependência

Toda a arquitetura se resume a uma regra:

> **As dependências de código só podem apontar para dentro.**

```
┌─────────────────────────────────────┐
│  api/          (HTTP, FastAPI)       │
│  ┌───────────────────────────────┐  │
│  │  infrastructure/  (DB, SMTP)  │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │  application/           │  │  │
│  │  │  (casos de uso)         │  │  │
│  │  │  ┌───────────────────┐  │  │  │
│  │  │  │  domain/          │  │  │  │
│  │  │  │  (regras puras)   │  │  │  │
│  │  │  └───────────────────┘  │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

O `domain/` não importa nada das camadas externas. A `infrastructure/` implementa contratos definidos pela `application/`. A `api/` apenas traduz HTTP para chamadas de serviço.

---

## As quatro camadas

### `domain/` — O que o negócio é

Contém entidades, exceções e validações puras. Nenhuma dependência externa.

```python
@dataclass
class Booking:
    id: UUID
    room_id: UUID
    start_at: datetime
    end_at: datetime
    status: str

def validate_booking_dates(start_at: datetime, end_at: datetime):
    if start_at >= end_at:
        raise InvalidDateError("start_at deve ser anterior a end_at")
```

Testável com `pytest` puro — sem banco, sem FastAPI, sem nada.

### `application/` — O que o sistema faz

Orquestra domain e repositórios. Contém os casos de uso e depende apenas de abstrações (interfaces/ABCs), nunca de implementações concretas.

```python
class BookingService:
    def __init__(self, booking_repo: BookingRepository):
        self.booking_repo = booking_repo  # ABC, não SQLAlchemy

    async def create(self, data: BookingCreate) -> Booking:
        validate_booking_dates(data.start_at, data.end_at)  # domain
        overlap = await self.booking_repo.find_overlap(...)  # interface
        if overlap:
            raise OverlapError("Sala já reservada nesse horário")
        return await self.booking_repo.create(data)
```

### `infrastructure/` — Como as coisas são feitas de verdade

Implementa as interfaces definidas em `application/`. É aqui que entram SQLAlchemy, asyncpg, bcrypt, aiosmtplib.

```python
class SQLAlchemyBookingRepository(BookingRepository):  # implementa o ABC
    async def find_overlap(self, room_id, start_at, end_at):
        result = await self.session.execute(
            select(BookingModel).where(...)
        )
        return result.scalar_one_or_none()
```

### `api/` — Como o mundo externo acessa

Traduz HTTP para casos de uso. Sem lógica de negócio.

```python
@router.post("/bookings", response_model=BookingOut, status_code=201)
async def create_booking(data: BookingCreate, service: BookingServiceDep):
    return await service.create(data)
```

---

## Comparação: Clean Architecture vs MVC clássico

### MVC clássico (Rails, Django ORM, Laravel)

```
Request
  │
  ▼
Controller
  │
  ▼
Model ──── regras de negócio
       ├── validações
       ├── queries SQL
       └── callbacks (before_save, after_create...)
  │
  ▼
View / Response
```

O Model concentra tudo: estado, comportamento, persistência e eventos. É conveniente para começar, mas escala mal — qualquer mudança no banco pode quebrar uma regra de negócio, e qualquer regra de negócio nova exige abrir o Model.

### Clean Architecture (este projeto)

```
Request
  │
  ▼
api/routers/         ← só traduz HTTP
  │
  ▼
application/services/ ← orquestra os casos de uso
  │           │
  ▼           ▼
domain/    application/interfaces/   ← contrato (ABC)
(regras)        │
                ▼
         infrastructure/repositories/ ← SQL aqui, isolado
```

Cada responsabilidade tem um lugar fixo. Mudar o banco não toca as regras. Mudar as regras não toca o banco.

### Tabela comparativa

| Aspecto | MVC clássico | Clean Architecture |
|---|---|---|
| Onde ficam as regras de negócio | No Model | Em `domain/` e `application/` |
| Dependência do framework | Alta (Model herda do ORM) | Baixa (domain não importa nada externo) |
| Testabilidade | Requer banco ou mock pesado | Domain testável com pytest puro |
| Trocar banco de dados | Impacta Model inteiro | Só reimplementa o repositório |
| Curva de entrada | Baixa | Média |
| Escala bem com complexidade | Não | Sim |

---

## Comparação: Clean Architecture vs Arquitetura Hexagonal

A **Hexagonal Architecture** (Ports & Adapters, Alistair Cockburn) resolve o mesmo problema com uma metáfora diferente:

```
        [ HTTP ]  [ CLI ]  [ Testes ]
             \       |       /
              \      |      /
           ┌──────────────────┐
           │   <<driving>>    │  ← Adapters primários
           │   Ports          │
           │ ┌──────────────┐ │
           │ │ Application  │ │  ← Núcleo (domain + use cases)
           │ └──────────────┘ │
           │   Ports          │
           │  <<driven>>      │  ← Adapters secundários
           └──────────────────┘
              /      |      \
             /       |       \
        [ DB ]  [ SMTP ]  [ Redis ]
```

- **Ports** são as interfaces (ABCs) — o contrato que o núcleo expõe
- **Adapters** são as implementações concretas — HTTP, SQL, SMTP
- **Driving side**: quem inicia a ação (HTTP request, CLI command, teste)
- **Driven side**: quem é acionado pelo núcleo (banco, e-mail, fila)

### Tabela comparativa

| Aspecto | Clean Architecture | Hexagonal |
|---|---|---|
| Metáfora central | Camadas concêntricas | Lados do hexágono (driving / driven) |
| Nomenclatura | domain, application, infrastructure | core, ports, adapters |
| Foco | Direção das dependências | Isolamento do núcleo de qualquer I/O |
| Diferença prática | Quase nenhuma — são complementares | Quase nenhuma — são complementares |

Na prática, os dois modelos chegam à mesma estrutura. Clean Architecture nomeia as camadas, Hexagonal nomeia os pontos de entrada e saída.

---

## Comparação: Clean Architecture vs DDD

**Domain-Driven Design** não é uma estrutura de pastas — é uma filosofia de modelagem. O DDD define como nomear e organizar o código baseado no vocabulário do negócio.

| Conceito DDD | O que significa | No nosso projeto |
|---|---|---|
| Linguagem ubíqua | Usar os mesmos termos do negócio no código | `Booking`, `Room`, `Organizer` — não `Record`, `Entry` |
| Entity | Objeto com identidade única ao longo do tempo | `Booking`, `User`, `Room` (todos com UUID) |
| Value Object | Objeto sem identidade, definido pelos seus valores | `tstzrange` do PostgreSQL, duração de reserva |
| Aggregate | Cluster de entidades com uma raiz que controla o acesso | `Booking` + `BookingParticipant` — Booking é a raiz |
| Repository | Abstração de coleção de aggregates | `BookingRepository (ABC)` em `application/interfaces/` |
| Domain Service | Lógica que não pertence a uma entidade só | `validate_booking_dates()` em `domain/validators.py` |
| Domain Event | Fato que aconteceu no domínio | `outbox_events` (BOOKING_CREATED, BOOKING_CANCELED) |
| Bounded Context | Fronteira de um subdomínio | Não aplicado formalmente (app pequena) |

### O que usamos de DDD neste projeto

- Nomes das entidades refletem o domínio de negócio
- Repositórios como abstrações em `application/interfaces/`
- Exceções de domínio (`OverlapError`, `InvalidDateError`) em vez de exceções genéricas
- Eventos de domínio implícitos via Outbox (`outbox_events`)

### O que não usamos

- Aggregates formais com invariantes encapsuladas
- Value Objects como classes próprias
- Bounded Contexts (seria relevante se o sistema fosse maior)
- Event Sourcing

---

## Por que escolhemos Clean Architecture aqui

1. **Testabilidade**: regras de negócio testáveis sem infraestrutura — essencial para CI rápido
2. **Isolamento de mudanças**: trocar banco ou framework não propaga para o domínio
3. **Clareza de responsabilidade**: cada arquivo tem um papel bem definido
4. **Escala com complexidade**: quando o sistema crescer, a estrutura já está preparada

O custo é a verbosidade inicial — mais arquivos, mais interfaces. Para sistemas pequenos pode parecer excessivo, mas o ganho aparece quando a complexidade aumenta.
