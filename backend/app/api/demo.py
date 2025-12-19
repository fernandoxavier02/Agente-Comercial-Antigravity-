"""
Endpoint de Simulação: Gera leads de exemplo baseados no SignalsCollector
"""

from fastapi import APIRouter
from datetime import datetime, timezone
from typing import List
from ..schemas import LeadClassification, PainPoint, Stage, Maturity, Scores, Evidence, VisualAnalysis, CategoryScore

router = APIRouter()

@router.get("/demo-leads", response_model=List[LeadClassification])
def get_demo_leads():
    """
    Retorna leads de demonstração simulando captura do SignalsCollector.
    Inclui diferentes camadas de intenção e wealth scores.
    """
    
    demo_leads = [
        # Lead 1: Ultra Luxury (St. Tropez + Jardins)
        LeadClassification(
            lead_id="LEAD-2025-001",
            source="instagram_comment",
            source_url="https://instagram.com/p/example1",
            author_handle="@luxury_traveler",
            timestamp=datetime.now(timezone.utc),
            text_excerpt="Alguém já fez Ultraformer no Jardins? Voltando de St. Tropez e quero manter o glow! 🌟",
            pain_point=PainPoint(label="Flacidez facial", confidence=0.85),
            intent_stage=Stage(label="consideration", confidence=0.90),
            maturity=Maturity(label="advanced", score=85),
            scores=Scores(
                fit=95,
                intent=90,
                urgency=75,
                risk=5,
                lead_score=92,
                evidence_quality=88
            ),
            visual_analysis=VisualAnalysis(
                wealth_score=98,
                visual_fit_score=95,
                categories={
                    "skin_glow": CategoryScore(score=92, justification="Pele bem cuidada, sinais de tratamentos prévios"),
                    "lifestyle_indicators": CategoryScore(score=98, justification="Menção a St. Tropez indica viagens de luxo"),
                },
                tags=["ultra_high_net_worth", "luxury_traveler", "jardins_sp", "dog_whistle:st_tropez"],
                technical_justification="Lead de altíssima prioridade. Contexto de viagem de luxo + busca ativa em bairro nobre.",
                red_flags=[]
            ),
            evidence=[
                Evidence(
                    text="Menção explícita a St. Tropez (destino de elite)",
                    url="https://instagram.com/p/example1"
                )
            ],
            risk_flags=[],
            version="v2.0"
        ),
        
        # Lead 2: Premium (Fasano + Itaim)
        LeadClassification(
            lead_id="LEAD-2025-002",
            source="instagram_comment",
            source_url="https://instagram.com/p/example2",
            author_handle="@socialite_sp",
            timestamp=datetime.now(timezone.utc),
            text_excerpt="Acabei de voltar do Fasano e vi uma amiga com a pele incrível. Ela disse que fez Morpheus 8 no Itaim.",
            pain_point=PainPoint(label="Rejuvenescimento", confidence=0.80),
            intent_stage=Stage(label="discovery", confidence=0.75),
            maturity=Maturity(label="intermediate", score=70),
            scores=Scores(
                fit=88,
                intent=75,
                urgency=60,
                risk=10,
                lead_score=80,
                evidence_quality=82
            ),
            visual_analysis=VisualAnalysis(
                wealth_score=85,
                visual_fit_score=88,
                categories={
                    "skin_glow": CategoryScore(score=85, justification="Interesse em procedimentos avançados"),
                    "lifestyle_indicators": CategoryScore(score=90, justification="Frequenta Fasano (hotel 5 estrelas)"),
                },
                tags=["premium", "lifestyle_premium", "itaim_sp", "dog_whistle:fasano"],
                technical_justification="Lead premium. Frequenta ambientes de luxo e busca procedimentos de alto padrão.",
                red_flags=[]
            ),
            evidence=[
                Evidence(
                    text="Menção ao Hotel Fasano (indicador de alto padrão)",
                    url="https://instagram.com/p/example2"
                )
            ],
            risk_flags=[],
            version="v2.0"
        ),
        
        # Lead 3: Intenção Direta (Google Search)
        LeadClassification(
            lead_id="LEAD-2025-003",
            source="google_search",
            source_url="https://google.com/search?q=melhor+clinica+ultraformer+jardins",
            author_handle="@ana_sp",
            timestamp=datetime.now(timezone.utc),
            text_excerpt="Qual a melhor clínica para Ultraformer no Jardins? Preciso de indicação urgente!",
            pain_point=PainPoint(label="Flacidez", confidence=0.90),
            intent_stage=Stage(label="decision", confidence=0.95),
            maturity=Maturity(label="advanced", score=80),
            scores=Scores(
                fit=85,
                intent=95,
                urgency=90,
                risk=5,
                lead_score=88,
                evidence_quality=85
            ),
            visual_analysis=VisualAnalysis(
                wealth_score=65,
                visual_fit_score=75,
                categories={
                    "skin_glow": CategoryScore(score=70, justification="Interesse em tecnologia específica (Ultraformer)"),
                    "lifestyle_indicators": CategoryScore(score=65, justification="Busca em bairro nobre, mas sem Dog Whistles"),
                },
                tags=["direct_intent", "jardins_sp", "high_urgency"],
                technical_justification="Intenção de compra direta. Busca ativa por clínica específica em região premium.",
                red_flags=[]
            ),
            evidence=[
                Evidence(
                    text="Busca ativa no Google por clínica específica",
                    url="https://google.com/search?q=melhor+clinica+ultraformer+jardins"
                )
            ],
            risk_flags=[],
            version="v2.0"
        ),
        
        # Lead 4: Community (Baixa Prioridade)
        LeadClassification(
            lead_id="LEAD-2025-004",
            source="facebook_group",
            source_url="https://facebook.com/groups/estetica/posts/123",
            author_handle="@maria_santos",
            timestamp=datetime.now(timezone.utc),
            text_excerpt="Quero muito fazer harmonização! Alguém tem experiência?",
            pain_point=PainPoint(label="Harmonização facial", confidence=0.70),
            intent_stage=Stage(label="discovery", confidence=0.60),
            maturity=Maturity(label="beginner", score=40),
            scores=Scores(
                fit=50,
                intent=60,
                urgency=40,
                risk=15,
                lead_score=52,
                evidence_quality=55
            ),
            visual_analysis=VisualAnalysis(
                wealth_score=35,
                visual_fit_score=45,
                categories={
                    "skin_glow": CategoryScore(score=50, justification="Interesse genérico, sem especificidade"),
                    "lifestyle_indicators": CategoryScore(score=30, justification="Sem indicadores de luxo ou geolocalização premium"),
                },
                tags=["community", "beginner", "low_priority"],
                technical_justification="Lead de baixa prioridade. Fase inicial de descoberta sem contexto de alto padrão.",
                red_flags=[]
            ),
            evidence=[
                Evidence(
                    text="Pergunta genérica em grupo de Facebook",
                    url="https://facebook.com/groups/estetica/posts/123"
                )
            ],
            risk_flags=[],
            version="v2.0"
        ),
    ]
    
    return demo_leads
