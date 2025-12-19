"""
SignalsCollector - Motor de Inteligência de Fontes
Implementa Taxonomia de Intenção em 3 Camadas para captura estratégica de leads.
"""

from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel

class MissionType(str, Enum):
    """Tipos de missões de coleta de sinais"""
    SOCIAL = "social"  # Instagram, TikTok, Grupos
    TECHNICAL = "technical"  # Blogs, Fóruns Médicos, Reviews
    LOCATION = "location"  # Geolocalização (Bairros de Elite SP)
    LUXURY = "luxury"  # Dog Whistles de Lifestyle Premium

class IntentLayer(str, Enum):
    """Camadas de Intenção de Compra"""
    DIRECT = "direct"  # "Qual a melhor clínica para X?"
    COMMUNITY = "community"  # "Quero muito fazer isso!"
    LIFESTYLE = "lifestyle"  # Contexto de luxo (St. Tropez, Verão em Mônaco)

class Signal(BaseModel):
    """Sinal capturado de uma fonte"""
    source: str  # "instagram_comment", "google_maps_review", etc.
    content: str  # Texto do post/comentário
    author_handle: str
    url: str
    intent_layer: IntentLayer
    mission_type: MissionType
    geo_context: str | None = None  # "Jardins, SP"
    luxury_indicators: List[str] = []  # ["hermès", "jato_executivo"]
    timestamp: str

class MissionConfig(BaseModel):
    """Configuração de uma Missão de Busca"""
    mission_type: MissionType
    enabled: bool = True
    sources: List[str]  # ["instagram", "google_maps", "forums"]
    keywords: List[str]  # Termos de busca
    geo_filters: List[str] = []  # ["Jardins", "Itaim Bibi"]
    dog_whistles: List[str] = []  # Indicadores de luxo

# ===== CONFIGURAÇÕES PRÉ-DEFINIDAS =====

MISSION_CONFIGS = {
    "social": MissionConfig(
        mission_type=MissionType.SOCIAL,
        sources=["instagram_comments", "tiktok_comments", "facebook_groups"],
        keywords=[
            "quero muito fazer",
            "alguém já fez",
            "recomendação de clínica",
            "harmonização facial",
            "ultraformer",
            "morpheus8"
        ],
        geo_filters=["São Paulo", "Jardins", "Itaim", "Vila Olímpia"],
    ),
    
    "technical": MissionConfig(
        mission_type=MissionType.TECHNICAL,
        sources=["google_search", "google_maps_reviews", "medical_forums"],
        keywords=[
            "melhor clínica para ultraformer",
            "review morpheus 8 são paulo",
            "preço harmonização facial jardins",
            "clínica estética alto padrão sp"
        ],
        geo_filters=["Paraíso", "Jardins", "Itaim Bibi", "Moema"],
    ),
    
    "luxury": MissionConfig(
        mission_type=MissionType.LUXURY,
        sources=["casa_vogue", "forbes_life", "instagram_luxury_profiles"],
        keywords=[
            "protocolo de rejuvenescimento",
            "preparação para evento",
            "estética médica de luxo"
        ],
        dog_whistles=[
            "st. tropez",
            "mônaco",
            "verão europeu",
            "yacht week",
            "hermès",
            "cartier",
            "jato executivo",
            "classe executiva",
            "fasano",
            "unique hotel"
        ],
    ),
}

# ===== DOG WHISTLES (Indicadores de Alto Padrão) =====

DOG_WHISTLES = {
    "travel": ["st. tropez", "mônaco", "dubai", "maldivas", "aspen", "courchevel"],
    "brands": ["hermès", "chanel", "cartier", "patek philippe", "rolex", "loro piana"],
    "transport": ["jato executivo", "classe executiva", "primeira classe", "iate"],
    "venues_sp": ["fasano", "unique hotel", "hotel emiliano", "l'hotel", "tivoli mofarrej"],
    "lifestyle": ["yacht week", "polo", "golfe", "tênis no clube", "spa day"],
}

class SignalsCollector:
    """
    Motor de Coleta de Sinais com Taxonomia de Intenção.
    Orquestra as missões de busca e classifica os sinais capturados.
    """
    
    def __init__(self):
        self.missions = MISSION_CONFIGS
        self.dog_whistles = DOG_WHISTLES
    
    def classify_intent_layer(self, content: str, source: str) -> IntentLayer:
        """
        Classifica o sinal em uma das 3 camadas de intenção.
        """
        content_lower = content.lower()
        
        # Layer 1: Intenção Direta (Busca ativa por clínica)
        direct_signals = ["melhor clínica", "qual clínica", "preço", "review", "recomendação"]
        if any(signal in content_lower for signal in direct_signals):
            return IntentLayer.DIRECT
        
        # Layer 3: Lifestyle (Dog Whistles de Luxo)
        luxury_signals = [dw for category in self.dog_whistles.values() for dw in category]
        if any(signal in content_lower for signal in luxury_signals):
            return IntentLayer.LIFESTYLE
        
        # Layer 2: Community (Default para redes sociais)
        return IntentLayer.COMMUNITY
    
    def detect_luxury_indicators(self, content: str) -> List[str]:
        """
        Detecta Dog Whistles de luxo no conteúdo.
        """
        content_lower = content.lower()
        detected = []
        
        for category, whistles in self.dog_whistles.items():
            for whistle in whistles:
                if whistle in content_lower:
                    detected.append(f"{category}:{whistle}")
        
        return detected
    
    def should_prioritize(self, signal: Signal) -> bool:
        """
        Define se um sinal deve ter prioridade máxima.
        Critérios: Intenção Direta + Geo SP + Luxury Indicators.
        """
        return (
            signal.intent_layer == IntentLayer.DIRECT and
            signal.geo_context in ["Jardins", "Itaim Bibi", "Paraíso", "Vila Olímpia"] and
            len(signal.luxury_indicators) > 0
        )
    
    async def execute_mission(self, mission_name: str) -> List[Signal]:
        """
        Executa uma missão de coleta.
        (Placeholder - será implementado com scrapers reais)
        """
        config = self.missions.get(mission_name)
        if not config or not config.enabled:
            return []
        
        # TODO: Implementar scrapers específicos por fonte
        # Por enquanto, retorna lista vazia
        return []

# ===== EXEMPLO DE USO =====
if __name__ == "__main__":
    collector = SignalsCollector()
    
    # Simular um sinal capturado
    test_signal = Signal(
        source="instagram_comment",
        content="Alguém já fez Ultraformer no Jardins? Voltando de St. Tropez e quero manter o glow!",
        author_handle="@luxury_traveler",
        url="https://instagram.com/p/example",
        intent_layer=collector.classify_intent_layer(
            "Alguém já fez Ultraformer no Jardins? Voltando de St. Tropez e quero manter o glow!",
            "instagram"
        ),
        mission_type=MissionType.SOCIAL,
        geo_context="Jardins",
        luxury_indicators=collector.detect_luxury_indicators(
            "Alguém já fez Ultraformer no Jardins? Voltando de St. Tropez e quero manter o glow!"
        ),
        timestamp="2025-12-18T19:00:00"
    )
    
    print(f"Intent Layer: {test_signal.intent_layer}")
    print(f"Luxury Indicators: {test_signal.luxury_indicators}")
    print(f"High Priority: {collector.should_prioritize(test_signal)}")
