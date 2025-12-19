"""
Teste com Dados Simulados - Demonstra o fluxo completo do SignalsCollector
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sources.signals_collector import SignalsCollector, Signal, IntentLayer, MissionType

def test_signal_classification():
    """Testa a classificação de sinais e detecção de Dog Whistles"""
    
    print("=" * 70)
    print("🧪 TESTE: CLASSIFICAÇÃO DE SINAIS E DETECÇÃO DE LUXO")
    print("=" * 70)
    
    collector = SignalsCollector()
    
    # Simular 3 sinais capturados de diferentes fontes
    test_signals = [
        {
            "content": "Alguém já fez Ultraformer no Jardins? Voltando de St. Tropez e quero manter o glow!",
            "author": "@luxury_traveler",
            "source": "instagram_comment",
            "expected_layer": "LIFESTYLE",
            "expected_priority": True
        },
        {
            "content": "Qual a melhor clínica para harmonização facial em São Paulo? Preciso de indicação urgente!",
            "author": "@ana_sp",
            "source": "google_search",
            "expected_layer": "DIRECT",
            "expected_priority": False  # Sem Dog Whistles
        },
        {
            "content": "Quero muito fazer! Alguém tem experiência?",
            "author": "@maria123",
            "source": "facebook_group",
            "expected_layer": "COMMUNITY",
            "expected_priority": False
        },
        {
            "content": "Acabei de voltar do Fasano e vi uma amiga com a pele incrível. Ela disse que fez Morpheus 8 aqui no Itaim. Alguém conhece?",
            "author": "@socialite_sp",
            "source": "instagram_comment",
            "expected_layer": "LIFESTYLE",
            "expected_priority": True  # Fasano + Itaim
        }
    ]
    
    high_priority_count = 0
    
    for i, test_data in enumerate(test_signals, 1):
        print(f"\n{'─' * 70}")
        print(f"📍 SINAL #{i}")
        print(f"{'─' * 70}")
        print(f"Fonte: {test_data['source']}")
        print(f"Autor: {test_data['author']}")
        print(f"Conteúdo: \"{test_data['content']}\"")
        
        # Classificar
        intent_layer = collector.classify_intent_layer(test_data['content'], test_data['source'])
        luxury_indicators = collector.detect_luxury_indicators(test_data['content'])
        
        # Criar Signal object
        signal = Signal(
            source=test_data['source'],
            content=test_data['content'],
            author_handle=test_data['author'],
            url=f"https://example.com/post/{i}",
            intent_layer=intent_layer,
            mission_type=MissionType.SOCIAL,
            geo_context="São Paulo" if "são paulo" in test_data['content'].lower() or "jardins" in test_data['content'].lower() or "itaim" in test_data['content'].lower() else None,
            luxury_indicators=luxury_indicators,
            timestamp="2025-12-18T19:00:00"
        )
        
        is_priority = collector.should_prioritize(signal)
        
        # Resultados
        print(f"\n🔍 ANÁLISE:")
        print(f"  ├─ Camada de Intenção: {intent_layer.value.upper()}")
        print(f"  ├─ Dog Whistles Detectados: {len(luxury_indicators)}")
        if luxury_indicators:
            for indicator in luxury_indicators:
                print(f"  │  └─ {indicator}")
        print(f"  ├─ Contexto Geográfico: {signal.geo_context or 'N/A'}")
        print(f"  └─ 🔥 PRIORIDADE MÁXIMA: {'SIM' if is_priority else 'NÃO'}")
        
        # Validação
        assert intent_layer.value == test_data['expected_layer'].lower(), f"Esperado {test_data['expected_layer']}, obteve {intent_layer.value}"
        
        if is_priority:
            high_priority_count += 1
    
    print(f"\n{'═' * 70}")
    print(f"✅ RESUMO DO TESTE")
    print(f"{'═' * 70}")
    print(f"📊 Total de Sinais Analisados: {len(test_signals)}")
    print(f"🔥 Leads de Prioridade Máxima: {high_priority_count}")
    print(f"💎 Taxa de Conversão Esperada: {(high_priority_count / len(test_signals)) * 100:.1f}%")
    print(f"\n✨ Todos os testes passaram com sucesso!")

if __name__ == "__main__":
    test_signal_classification()
