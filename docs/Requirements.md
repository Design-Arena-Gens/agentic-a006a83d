## EsthetiManage - Requisitos de Produto

### Visão Geral
- Plataforma SaaS para clínicas de estética com foco em automação de agendamentos, relacionamento com pacientes e inteligência operacional.

### Principais Funcionalidades
- Agendamentos online com detecção de conflitos, confirmação e reagendamentos.
- Lembretes automatizados via SMS e e-mail, com templates personalizáveis.
- CRM de pacientes com histórico de tratamentos, preferências e anotações.
- Gestão de estoque de produtos e insumos, alertas de reposição.
- Faturamento com integração Stripe para pagamentos online e in-clínica.
- Relatórios operacionais e financeiros com dashboards analíticos.
- Portal do paciente com agenda, pagamentos e histórico.
- Painel administrativo com controle de usuários, permissões e métricas.

### Perfis de Usuário
- **Admin:** Configurações gerais, gestão financeira, relatórios completos.
- **Esteticista:** Visualização de agenda, registros clínicos, atualização de estoque.
- **Recepcionista:** Controle de agendamentos, check-in, lembretes.
- **Paciente:** Agendamento, pagamentos, histórico de tratamentos.

### Considerações Técnicas
- Backend: FastAPI + PostgreSQL + SQLAlchemy + JWT Auth.
- Frontend: React/Next.js + Tailwind CSS + Axios + i18n PT-BR.
- Integrações: Twilio (SMS), Stripe (pagamentos), Google Calendar (sincronização).
- Testes: Pytest (backend), Cypress (frontend) com cobertura mínima de 80%.
- Segurança: Conformidade LGPD, logs auditáveis, monitoramento Sentry.
- Deploy: Backend em contêiner (Docker), Frontend em Vercel, CI/CD GitHub Actions.
