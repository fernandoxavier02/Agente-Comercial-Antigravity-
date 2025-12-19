# Agente de Captação por Intenção — Estética Médica (MVP + Camadas)

Este documento descreve a **essência do agente** e a **arquitetura do produto SaaS** para captação e qualificação de potenciais clientes em **Saúde & Beleza / Medicina Estética** (pele, injetáveis, lasers, bioestimuladores, redução de gordura localizada etc.).

> **Tese central**: o agente não “vende tratamento”. Ele detecta **intenção/dor estética**, **qualifica** e sugere **abordagem personalizada e segura** (sem diagnóstico, sem promessas, com compliance).

---

## 1) Objetivos do produto

### Objetivos (MVP)
1. **Detectar dor estética latente** em redes sociais/web (textos públicos).
2. **Classificar intenção e fit** com o ICP da clínica.
3. **Sugerir abordagem** (estratégia + rascunho de mensagem) com base no contexto público.
4. Entregar ao time comercial uma **lista acionável** de leads: *por que entrou, score, dor, abordagem sugerida, evidências (trechos/link), rascunho de mensagem*.

### Não-objetivos (por padrão)
- Disparar mensagens automaticamente (no MVP: **human-in-the-loop**).
- Fazer diagnóstico ou prescrição.
- Coletar dados sensíveis (saúde, raça, religião etc.) ou inferi-los.
- Bypassar termos de uso de plataformas.

---

## 2) Camadas de valor (do “buscador” ao produto defensável)

### Camada 1 — Inteligência de intenção estética (latente)
- Detectar sinais indiretos (“minha pele mudou”, “melasma”, “flacidez”, “olheiras”, “celulite”, “bigode chinês”, “papada”, “estrias”, “queda de colágeno”).
- Classificar **estado emocional** (curiosidade, frustração, comparação, urgência) + **momento de compra** (descoberta → consideração → decisão).

### Camada 2 — Tradução “dor → classes de tratamento”
- Mapear dor para **classes** (ex.: bioestimuladores, laser, ultrassom microfocado, peelings, skinboosters), sem prometer resultado.
- Produzir “hipóteses de conversa” (educacional) e **perguntas de triagem** para recepção/comercial.

### Camada 3 — Perfil de maturidade estética do lead
- Classificar: primeiro contato vs recorrente; conservador vs arrojado; naturalidade vs impacto; sensível a preço vs sensível a qualidade.
- Gerar **Maturity Score** (0–100) + “porquê”.

### Camada 4 — Inteligência de abordagem (anti-spam)
- Recomendar **estilo** de contato: acolhimento, educacional, autoridade médica, conversacional.
- Gerar mensagem baseada em **evidência concreta** (o que a pessoa escreveu) + **CTA leve**.

### Camada 5 — Conteúdo para aquecimento
- Sugerir mini-conteúdos (“o que é melasma”, “por que colágeno cai após 40”, “bioestimulador: o que é”) para uso do time/clinica.

### Camada 6 — Radar de tendências
- Painel: dores/temas em alta, objeções, termos emergentes, sazonalidade, por região/raio.

### Camada 7 — Copiloto de recepção/comercial
- Sugestões de respostas (WhatsApp/DM), objeções, agendamento, follow-up.

### Camada 8 — Compliance médico + LGPD (blindagem)
- Guardrails: evitar promessas (“garante”), evitar diagnóstico, linguagem educativa, opt-out, logs de justificativa.

---

## 3) Arquitetura — visão geral

### 3.1 Componentes principais

**A) Coleta (Signals Collector)**
- Conectores por fonte (rede social / web / fóruns).
- Estratégia: *listen/search* por tópicos e padrões semânticos (não só keywords).
- Saída: “candidatos” (post/comentário) + metadados públicos (link, autor, timestamp, texto).

**B) Normalização & Deduplicação**
- Limpeza de texto, idioma, remoção de spam.
- Dedup por hash (texto + link + autor) e similaridade semântica.

**C) Classificação (Intent Engine)**
- Classificar:
  - **Dor estética** (taxonomia)
  - **Intenção** (descoberta/consideração/decisão)
  - **Fit** com ICP (persona, localização aproximada se pública, linguagem, contexto)
  - **Risco** (conteúdo sensível / menor de idade / saúde sensível)
- Saída: rótulos + probabilidades + justificativas (“evidências”).

**D) Enriquecimento (Context Enricher)**
- Busca de contexto **público** adicional:
  - histórico recente do autor (limitado e dentro de ToS)
  - contexto do tópico/comunidade
  - menções a experiências e preferências
- Saída: “lead card” com resumo, sem armazenar excessos.

**E) Scoring & Priorização**
- Score final: `LeadScore = w1*Fit + w2*Intent + w3*Urgency + w4*Maturity - w5*Risk`
- Score de **qualidade de evidência** (confiança).

**F) Abordagem & Mensagem (Outreach Composer)**
- Define estratégia (tom, formato, CTA).
- Gera:
  - 1–3 variações de mensagem curta
  - 1 variação “educacional” com link interno/conteúdo
  - Perguntas de triagem para recepção

**G) Painel SaaS (UI)**
- Lista priorizada de leads
- “Por que esse lead entrou” (evidência)
- Botão: copiar mensagem / exportar / criar tarefa
- Trilhas: “Aquecimento” e “Follow-up”

**H) Observabilidade & Auditoria**
- Logs por lead: inputs, versões do prompt/modelo, scores, decisões de bloqueio, opt-outs.

---

### 3.2 Fluxo (pipeline)

1. **Scheduler** dispara buscas por tópico/consulta.
2. Conector coleta posts/comentários públicos.
3. Normaliza/dedup.
4. Classifica dor/intenção/fit/risco.
5. Enriquecimento leve (contexto público adicional).
6. Scoring final.
7. Geração de abordagem + mensagens.
8. Entrega no painel + export/integração.

---

## 4) Taxonomias essenciais (para o domínio)

### 4.1 Taxonomia de dores (exemplos)
- **Pele/qualidade**: melasma, manchas, acne, cicatrizes, rosácea, poros, textura, “viço”
- **Envelhecimento**: flacidez, rugas, linhas finas, perda de colágeno
- **Volume/contorno**: olheiras, sulcos, bigode chinês, mandíbula, queixo, papada
- **Corpo**: gordura localizada, celulite, estrias, flacidez corporal
- **Pós-procedimento**: dúvidas, medo, arrependimento, comparação
- **Objeções**: dor, preço, medo de ficar artificial, segurança

### 4.2 Intenção (estágios)
- Descoberta: “alguém sabe”, “o que funciona”, “dúvida”
- Consideração: “entre X e Y”, “vale a pena”, “qual clínica”
- Decisão: “indicação”, “onde fazer”, “alguém já fez com Dr(a) …”

### 4.3 Maturidade estética
- Iniciante / Intermediário / Avançado
- Atributos: aversão a agulha, preferências (naturalidade), tolerância a downtime, sensibilidade a preço.

---

## 5) Compliance & Segurança (mínimo necessário no MVP)

### 5.1 Regras de linguagem (mensagens)
- Proibido: promessas (“garantido”, “100%”, “resultado certo”).
- Proibido: diagnóstico (“você tem …”, “isso é …”).
- Obrigatório: convite para **avaliação** e tom educativo.
- CTA leve: “Se fizer sentido, posso te enviar informações / te colocar em contato com a equipe”.

### 5.2 Conteúdos a bloquear
- Indícios de **menor de idade**.
- Conteúdo explicitamente sensível (doenças, laudos, etc.) — tratar com extrema cautela; preferir excluir.
- Assédio, vulnerabilidade extrema, automutilação (bloquear e encaminhar política interna).

### 5.3 LGPD — postura prática
- Coletar apenas dados **publicamente disponíveis** e necessários.
- Minimização: armazenar somente o essencial (link, handle, trecho curto, scores).
- Opt-out: mecanismo simples de exclusão.
- Registro de base legal e finalidade; política de retenção.

> Nota: adequação completa exige assessoria jurídica. O MVP deve nascer com minimização, auditoria e opt-out.

---

## 6) Dados, Armazenamento e Modelo de domínio

### 6.1 Entidades (mínimo)
- `SourceItem`: {source, url, author_handle, timestamp, text, raw_metadata}
- `Lead`: {lead_id, source_item_id, clinic_id, scores, labels, evidence_snippets}
- `OutreachDraft`: {lead_id, strategy, messages[], triage_questions[]}
- `AuditLog`: {event, actor, model_version, prompt_version, timestamps}

### 6.2 Retenção
- Texto completo: opcional e com limite; preferir armazenar apenas trechos.
- Reprocessamento: guardar apenas hashes + referências.

---

## 7) Integrações (fase 2)
- CRM (HubSpot/Pipedrive/Salesforce): criar lead + notas + tags.
- WhatsApp Business via provedor (somente após consentimento e compliance).
- Zapier/Make para automações.

---

## 8) Stack sugerida (neutra)

### Backend
- API: Python (FastAPI) ou Node (NestJS)
- Jobs: Celery/RQ (Python) ou BullMQ (Node)
- Filas: Redis
- Banco: Postgres
- Vetores (opcional): pgvector
- Observabilidade: OpenTelemetry + logs estruturados

### IA
- Classificação: prompts + modelos (LLM) + regras
- Embeddings: similaridade para dedup e cluster de tópicos
- Guardrails: validadores + políticas + classificadores de risco

### Frontend
- React/Next.js, dashboard simples e rápido.

---

## 9) Estratégia “human-in-the-loop” (indispensável no MVP)
1. O agente **sugere**: lead + score + porquê + mensagem.
2. O humano **aprova/edita** e escolhe canal.
3. Feedback vira treino:
   - “lead bom/ruim”
   - “mensagem boa/ruim”
   - “converteu/não converteu”

---

## 10) Avaliação (para não virar spam)
Métricas do MVP:
- Precisão de intenção (amostragem humana)
- Taxa de aprovação de lead (comercial aprova?)
- Taxa de resposta (reply rate)
- Taxa de agendamento
- Taxa de opt-out/denúncia (tem que ser baixíssima)
- Tempo poupado por SDR/recepção

---

## 11) MVP — escopo fechado (recomendado)
### Entregáveis
- 1–2 fontes iniciais (ex.: uma rede social + web fórum)
- Pipeline completo (coleta → classificação → scoring → mensagem → painel)
- Taxonomia de dores + intent + maturidade
- Guardrails e auditoria
- Export simples (CSV) + copiar mensagem

### Fora do MVP
- Disparo automático e automações agressivas
- Muitas redes simultâneas
- Enriquecimento pesado com dados pessoais

---

## 12) Roadmap incremental (depois do MVP)
1. Radar de tendências (Camada 6)
2. Conteúdo de aquecimento (Camada 5)
3. Copiloto de recepção (Camada 7)
4. Integrações CRM
5. Motor de experimentos (A/B de mensagem + feedback loop)
6. Multiclínica / multi-ICP / multi-cidade

---

## 13) “Definition of Done” (para a primeira versão)
- O agente gera **leads com justificativa** (evidência clara)
- O time consegue **agir** em < 30 segundos por lead
- Mensagens são **contextuais** e com linguagem **segura**
- Existe auditoria e opt-out
- Métricas mínimas coletadas (aprovação, resposta, agendamento)

---

## 14) Prompting (padrões que o sistema deve seguir)
- Sempre incluir: ICP da clínica, tom da marca, regras de compliance, e evidências do texto do lead.
- Saída sempre estruturada (JSON) para parsing:
  - labels, scores, evidences, risk_flags, strategy, drafts.

---

### Apêndice — exemplo de saída estruturada (JSON)
```json
{
  "lead_id": "L123",
  "pain_point": {"label": "melasma/manchas", "confidence": 0.86},
  "intent_stage": {"label": "consideration", "confidence": 0.72},
  "maturity": {"label": "beginner", "score": 35},
  "scores": {"fit": 78, "intent": 72, "urgency": 40, "risk": 10, "lead_score": 69},
  "evidence": [
    {"text": "alguém conseguiu melhorar melasma?", "url": "https://..."}
  ],
  "approach": {"style": "educational", "cta": "avaliacao", "do_not": ["promessas", "diagnostico"]},
  "drafts": [
    "Vi seu comentário sobre melasma. Existem diferentes causas e abordagens, e uma avaliação ajuda a definir o melhor caminho. Se fizer sentido, posso te enviar algumas informações gerais e, se você quiser, te coloco em contato com a equipe para uma avaliação."
  ],
  "triage_questions": [
    "Há quanto tempo você percebe as manchas?",
    "Você já tentou algum tratamento antes?",
    "Tem preferência por opções com pouco downtime?"
  ]
}
```

---

## 15) Nota final (posicionamento)
Posicionamento recomendado:
- **Inteligência de intenção estética + abordagem segura**, não “automação de spam”.
- Vende: **qualidade e timing**, não volume.
