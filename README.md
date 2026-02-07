# EsthetiManage

SaaS full-stack para clínicas de estética com automação de agendamentos, CRM de pacientes, estoque, faturamento e relatórios inteligentes.

## 🌐 Arquitetura

- **Frontend**: Next.js 16 (React 19), Tailwind CSS 4, React Query, Chart.js, i18n PT-BR.
- **Backend**: FastAPI, SQLAlchemy 2, PostgreSQL, JWT Auth, integrações Twilio/Stripe/Google Calendar.
- **Infra**: Docker Compose, GitHub Actions CI, deploy alvo (Vercel + contêiner backend).
- **Observabilidade**: Sentry pronto para configuração via `SENTRY_DSN`.

```
.
├── backend/          # FastAPI + SQLAlchemy + pytest
├── frontend/         # Next.js app (dashboard + portal paciente + admin panel)
├── docs/             # Documentação funcional
├── docker-compose.yml
└── .github/workflows # CI para backend/frontend
```

## 🚀 Execução Local

### 1. Dependências
- Python 3.11+
- Node.js 20+
- Docker (opcional, mas recomendado)

### 2. Variáveis de ambiente

Copie os exemplos e preencha os segredos conforme suas integrações:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

### 3. Ambiente com Docker

```bash
docker compose up --build
```

API disponível em `http://localhost:8000/docs`  
Frontend em `http://localhost:3000`

### 4. Rodando manualmente

**Backend**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

## ✅ Testes

- Backend: `cd backend && pytest`
- Frontend (CI): `npm run lint` e `npm run build`
- E2E/Cobertura: Cypress e OWASP ZAP prontos para futura integração (não incluídos nesta iteração).

## 🔌 Integrações

- **Stripe**: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
- **Twilio**: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`
- **Google Calendar**: `GOOGLE_SERVICE_ACCOUNT_FILE`

Quando não configuradas, os serviços executam em modo _mock friendly_ sem interromper o fluxo.

## 📄 Documentação

- Requisitos funcionais em `docs/Requirements.md`
- Swagger/OpenAPI em `http://localhost:8000/docs`

## 📦 Deploy

- Frontend: `vercel deploy --prod --token $VERCEL_TOKEN --name agentic-a006a83d`
- Backend: container Docker pronto para rodar em serviços como AWS ECS/Heroku.

---

EsthetiManage acelera a operação de clínicas de estética com foco em automação, personalização e dados acionáveis.
