from __future__ import annotations
from ..schemas import LeadClassification, OutreachDraft, Approach
from ..core.config import settings

def generate_outreach_draft(lead: LeadClassification) -> OutreachDraft:
    """Gera um draft simples (MVP local) sem chamar LLM.
    Substitua por chamada ao seu provedor de LLM + prompts/validação.
    """
    # Estratégia conservadora se houver flags
    if lead.risk_flags:
        style = "educational"
        cta = "send_info"
        do_not = ["promessas", "diagnostico", "pressao", "mensagens_repetidas"]
        drafts = [
            "Vi seu comentário e, se fizer sentido, posso te enviar algumas informações gerais (sem compromisso). "
            "Se você preferir não receber mensagens, é só me avisar que eu paro por aqui."
        ]
        triage = []
    else:
        # Heurística simples por estágio
        if lead.intent_stage.label == "decision":
            style = "conversational"
            cta = "invite_evaluation"
        elif lead.intent_stage.label == "consideration":
            style = "educational"
            cta = "invite_evaluation"
        else:
            style = "empathetic"
            cta = "ask_question"

        do_not = ["promessas", "diagnostico", "pitch_agressivo"]
        drafts = [
            f"Vi seu comentário sobre {lead.pain_point.label}. Em geral, uma avaliação ajuda a entender as causas e as opções (sem promessas). "
            "Se fizer sentido, posso te mandar informações gerais e você decide com calma.",
            "Vi que você comentou sobre esse tema. Se você quiser, me conta há quanto tempo isso te incomoda? "
            "Aí eu consigo te enviar informações mais direcionadas (sem compromisso)."
        ]
        triage = [
            "Há quanto tempo você percebe isso?",
            "Você já tentou algum tratamento antes?",
            "Você prefere opções com pouco downtime?"
        ]

    return OutreachDraft(
        lead_id=lead.lead_id,
        approach=Approach(style=style, cta=cta, do_not=do_not),
        drafts=drafts,
        triage_questions=triage,
        version=settings.COMPOSER_PROMPT_VERSION,
    )
