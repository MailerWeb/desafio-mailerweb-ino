# Booking System Frontend

Frontend em React para o sistema de gerenciamento de reservas de salas.

## Features

- ✅ Autenticação com JWT
- ✅ Registro e login de usuários
- ✅ Listagem e criação de salas
- ✅ CRUD completo de reservas
- ✅ Validação de conflitos de horários
- ✅ Notificações por email automáticas
- ✅ Interface responsiva e intuitiva
- ✅ Tratamento de erros e loading states
- ✅ Testes unitários e de integração

## Tecnologias

- **React 18** - UI library
- **React Router v6** - Client-side routing
- **Axios** - HTTP client
- **Vite** - Build tool
- **Vitest** - Testing framework
- **@testing-library/react** - Testing utilities

## Setup Local

### Pré-requisitos

- Node.js 16+
- npm ou yarn

### Instalação

1. Clone o repositório
2. Acesse a pasta frontend:

```bash
cd frontend
```

3. Instale as dependências:

```bash
npm install
```

4. Crie um arquivo `.env` baseado em `.env.example`:

```bash
cp .env.example .env
```

5. Configure a URL da API (padrão: http://localhost:8000)

### Desenvolvimento

Para iniciar o servidor de desenvolvimento:

```bash
npm run dev
```

A aplicação estará disponível em `http://localhost:3000`

### Build

Para gerar a build de produção:

```bash
npm run build
```

### Testes

Para executar os testes:

```bash
npm run test
```

Para ver os testes em modo UI:

```bash
npm run test:ui
```

Para gerar relatório de cobertura:

```bash
npm run coverage
```

## Estrutura de Pastas

```
src/
├── main.jsx                 # Entry point
├── App.jsx                  # Componente principal
├── App.css                  # Estilos globais
├── pages/                   # Páginas
│   ├── Login.jsx           # Página de login
│   ├── Register.jsx        # Página de registro
│   ├── Rooms.jsx           # Listagem de salas
│   ├── BookingList.jsx     # Listagem de reservas
│   ├── CreateBooking.jsx   # Criar reserva
│   └── EditBooking.jsx     # Editar reserva
├── components/             # Componentes reutilizáveis
│   ├── ProtectedRoute.jsx  # Rota protegida
│   ├── Navigation.jsx      # Navegação
│   ├── Navigation.css
│   └── Alert.jsx           # Alertas
├── services/               # Serviços HTTP
│   ├── api.js             # Configuração do Axios
│   └── auth.js            # Chamadas de API
├── utils/                  # Utilitários
│   └── formatters.js      # Funções de formatação
└── __tests__/             # Testes
    ├── Login.test.jsx
    ├── BookingList.test.jsx
    └── integration.test.js
```

## Uso

### Login/Registro

1. Clique em "Cadastre-se aqui" para criar uma nova conta
2. Preencha nome, email e senha
3. Após o cadastro, faça login com suas credenciais

### Salas

1. Acesse a seção "Salas" na navegação
2. Clique em "+ Nova Sala" para criar uma sala
3. Preencha o nome e capacidade

### Reservas

1. Acesse "Reservas" ou "Nova Reserva"
2. Preencha os dados:
   - Título da reunião
   - Sala
   - Data/hora de início e término
   - Participantes (emails)
3. Os participantes receberão notificação por email

### Editar/Cancelar Reservas

1. Na listagem de reservas, clique em "Editar" ou "Cancelar"
2. Alterações disparam notificação aos participantes

## Validações

- **Autenticação**: JWT obrigatório
- **Datas**: ISO 8601 com timezone
- **Duração**: Mínimo 15 minutos, máximo 8 horas
- **Conflitos**: Previne sobreposição de horários
- **Participantes**: Múltiplos emails separados por vírgula

## Integração com Backend

O frontend se comunica com a API backend em `http://localhost:8000`. Os endpoints esperados são:

- `POST /users/register` - Registrar usuário
- `POST /users/login` - Fazer login
- `GET /users/{id}` - Obter informações do usuário
- `GET /rooms/` - Listar salas
- `POST /rooms/` - Criar sala
- `GET /rooms/{id}` - Obter detalhes da sala
- `GET /bookings/` - Listar reservas
- `POST /bookings/` - Criar reserva
- `GET /bookings/{id}` - Obter detalhes da reserva
- `PUT /bookings/{id}` - Editar reserva
- `DELETE /bookings/{id}` - Cancelar reserva

### Autenticação

O token JWT é armazenado em `localStorage` e enviado automaticamente em todas as requisições HTTP através do header `Authorization: Bearer {token}`.

## Tratamento de Erros

- Erros de validação: Mensagens displayadas no formulário
- Erros de API: Alertas na página
- Erros 401: Redirecionamento automático para login
- Loading states: Indicadores visuais durante operações

## Performance

- Lazy loading de componentes
- Otimização de re-renders com React hooks
- Proxy para API no Vite (desenvolvimento)

## Testes

### Cobertura de Testes

- ✅ Login e autenticação
- ✅ Listagem e filtragem de reservas
- ✅ Validação de conflitos de horários
- ✅ Formatação de datas
- ✅ Componentes reutilizáveis

### Exemplo de Teste

```javascript
it('renders login form', () => {
  render(<Login setIsAuthenticated={() => {}} />)
  expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
})
```

## Deployment

### Docker

```bash
docker build -t booking-frontend .
docker run -p 3000:3000 booking-frontend
```

### Vercel/Netlify

1. Conecte seu repositório
2. Configure `npm run build` como comando de build
3. Configure `dist` como diretório de output

## Troubleshooting

### CORS Error

Se receber erro de CORS, certifique-se que:
1. Backend está rodando em http://localhost:8000
2. Backend tem CORS configurado para aceitar requests do frontend
3. URL da API no `.env` está correta

### Token Expirado

Se receber erro 401:
1. Faça logout e login novamente
2. Verifique ACCESS_TOKEN_EXPIRE_MINUTES no backend

### Falha ao carregar dados

Verifique:
1. Se o backend está rodando
2. Se a API URL está correta no `.env`
3. Se você está autenticado (token em localStorage)

## Licença

MIT
