# Contratos de Dados

Os contratos são a coluna vertebral do produto:
- tornam o agente previsível
- facilitam auditoria e debug
- permitem troca de modelo/provedor sem quebrar a aplicação

## Schemas
- `schemas/lead_classification.schema.json`
- `schemas/outreach_draft.schema.json`
- `schemas/feedback_event.schema.json`
- `schemas/audit_log.schema.json`

## Regra de ouro
Qualquer saída de IA deve:
1) validar contra schema
2) conter evidências (trecho + URL)
3) registrar versionamento (prompt/modelo)
