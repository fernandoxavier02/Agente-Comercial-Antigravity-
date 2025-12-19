# Estética Agent SaaS — Starter Repo (MVP)

Starter de repositório para o MVP do **Agente de Captação por Intenção (Estética Médica)**.

## O que vem aqui
- **backend/** FastAPI (API + contratos + endpoints do MVP)
- **worker/** Celery (pipeline de ingestão/classificação/rascunho)
- **prompts/** templates de prompts (classificação e composição)
- **schemas/** JSON Schemas (contratos de dados do agente)
- **dashboard/** esqueleto Next.js (lista de leads + detalhe)
- **infra/** docker-compose (Postgres + Redis) e scripts
- **docs/** documentação do produto e arquitetura

## Rodar local (sugestão)
1) Subir infra:
```bash
cd infra
docker compose up -d
```

2) Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

3) Worker:
```bash
cd worker
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
celery -A worker.celery_app worker --loglevel=INFO
```

4) Dashboard (opcional):
```bash
cd dashboard
npm i
cp .env.example .env.local
npm run dev
```

> **Importante**: o MVP é **human-in-the-loop**. Nada de disparo automático de mensagens por padrão.

## Compliance
Este repo inclui guardrails básicos e estrutura para auditoria/opt-out. Ainda assim, adequação completa exige revisão jurídica (LGPD) e respeito aos termos de uso das plataformas.
