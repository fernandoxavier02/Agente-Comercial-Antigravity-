# Prompts

Mantemos prompts versionados e parametrizáveis. O backend/worker deve carregar estes arquivos e substituir variáveis.

- `classifier/system.md` + `classifier/user.md` → gera `LeadClassification` (JSON)
- `composer/system.md` + `composer/user.md` → gera `OutreachDraft` (JSON)

Boas práticas:
- Sempre retornar **JSON válido**.
- Sempre incluir **evidências** (trecho + URL).
- Aplicar guardrails (sem diagnóstico, sem promessas, CTA leve, opt-out quando aplicável).
