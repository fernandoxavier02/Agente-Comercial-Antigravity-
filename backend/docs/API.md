# API (MVP)

## Endpoints
- `GET /health`
- `POST /leads` cria lead (normalmente o worker chamará isso)
- `GET /leads` lista leads
- `GET /leads/{lead_id}` detalhe
- `POST /leads/{lead_id}/drafts` gera rascunho (MVP: heurística local; depois: LLM)
- `GET /leads/{lead_id}/drafts`
- `POST /feedback` registra feedback do time

## Contratos
Ver pasta `/schemas`.
