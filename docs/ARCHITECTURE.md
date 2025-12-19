# Arquitetura (resumo operacional)

## Módulos
- **backend/**: API + store (MVP em arquivos) + endpoints para leads, drafts e feedback
- **worker/**: pipeline assíncrono (no MVP, mock ingestion)
- **prompts/**: templates e versionamento de prompts (classificador e composer)
- **schemas/**: JSON Schema para validar saídas do agente
- **dashboard/**: UI mínima para operar leads

## Próximo passo técnico (ordem sugerida)
1) Implementar um **connector real** para 1 fonte (público e permitido).
2) Trocar heurística do `generate_outreach_draft` por:
   - chamar LLM com `prompts/composer/*`
   - validar JSON contra `/schemas/outreach_draft.schema.json`
3) Implementar classificador via LLM no worker:
   - `prompts/classifier/*`
   - validar JSON contra `/schemas/lead_classification.schema.json`
4) Deduplicação por similaridade + caches.
5) Scoring calibrado com feedback do time.
6) Migrar store de arquivos → Postgres.

## Padrão de segurança (MVP)
- human-in-the-loop
- auditoria
- opt-out
- minimização de dados
