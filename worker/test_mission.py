"""
Script de Teste: Executa uma missão manualmente para validar o fluxo
Uso: python test_mission.py [social|technical|luxury]
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from tasks_missions import execute_social_mission, execute_technical_mission, execute_luxury_mission

def test_social():
    """Testa a Missão Social"""
    print("=" * 60)
    print("🎯 TESTANDO MISSÃO SOCIAL")
    print("=" * 60)
    
    result = execute_social_mission()
    print(f"\n✅ Resultado: {result}")
    print(f"📊 Sinais Capturados: {result.get('signals_captured', 0)}")
    print(f"🔥 Alta Prioridade: {result.get('high_priority', 0)}")

def test_technical():
    """Testa a Missão Técnica"""
    print("=" * 60)
    print("🔍 TESTANDO MISSÃO TÉCNICA")
    print("=" * 60)
    
    result = execute_technical_mission()
    print(f"\n✅ Resultado: {result}")
    print(f"📊 Sinais Capturados: {result.get('signals_captured', 0)}")

def test_luxury():
    """Testa a Missão Luxo"""
    print("=" * 60)
    print("💎 TESTANDO MISSÃO LUXO")
    print("=" * 60)
    
    result = execute_luxury_mission()
    print(f"\n✅ Resultado: {result}")
    print(f"📊 Sinais Capturados: {result.get('signals_captured', 0)}")

if __name__ == "__main__":
    mission_type = sys.argv[1] if len(sys.argv) > 1 else "social"
    
    if mission_type == "social":
        test_social()
    elif mission_type == "technical":
        test_technical()
    elif mission_type == "luxury":
        test_luxury()
    else:
        print("❌ Missão inválida. Use: social, technical ou luxury")
        sys.exit(1)
