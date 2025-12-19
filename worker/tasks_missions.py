"""
Celery Tasks para Coleta de Sinais
Executa as missões periodicamente e salva leads no banco de dados
"""

from celery import shared_task
import logging
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from sources.signals_collector import SignalsCollector, Signal, IntentLayer
    from sources.scrapers.instagram import InstagramScraper
    from sources.scrapers.google import GoogleScraper
    from sources.scrapers.luxury_media import LuxuryMediaScraper
except ImportError:
    # Fallback for direct execution
    from .sources.signals_collector import SignalsCollector, Signal, IntentLayer
    from .sources.scrapers.instagram import InstagramScraper
    from .sources.scrapers.google import GoogleScraper
    from .sources.scrapers.luxury_media import LuxuryMediaScraper

logger = logging.getLogger(__name__)

@shared_task(name="execute_social_mission")
def execute_social_mission():
    """
    Executa a Missão Social (Instagram, Facebook).
    Periodicidade sugerida: A cada 2 horas.
    """
    logger.info("🎯 Iniciando Missão Social...")
    
    collector = SignalsCollector()
    instagram_scraper = InstagramScraper()
    
    # Configuração (pode vir do .env)
    profiles_to_monitor = os.getenv("SOCIAL_INSTAGRAM_PROFILES", "merz_aesthetics,classysbrasil").split(",")
    keywords = os.getenv("SOCIAL_KEYWORDS", "quero,fazer,clínica,recomendação").split(",")
    
    all_signals = []
    
    for profile in profiles_to_monitor:
        profile = profile.strip()
        logger.info(f"Scraping @{profile}...")
        
        comments = instagram_scraper.scrape_profile_comments(
            profile_username=profile,
            max_posts=10,
            days_back=3,
            keywords=keywords
        )
        
        # Converter para Signal objects
        for comment_data in comments:
            signal = Signal(
                source=comment_data["source"],
                content=comment_data["content"],
                author_handle=comment_data["author_handle"],
                url=comment_data["post_url"],
                intent_layer=collector.classify_intent_layer(
                    comment_data["content"], 
                    comment_data["source"]
                ),
                mission_type="social",
                geo_context=None,  # TODO: Extrair do perfil do autor
                luxury_indicators=collector.detect_luxury_indicators(comment_data["content"]),
                timestamp=comment_data["timestamp"]
            )
            
            all_signals.append(signal)
    
    logger.info(f"✅ Missão Social concluída: {len(all_signals)} sinais capturados")
    
    # TODO: Salvar no banco de dados via API
    # for signal in all_signals:
    #     if collector.should_prioritize(signal):
    #         # Enviar para classificação LLM + VisionEngine
    #         pass
    
    return {"signals_captured": len(all_signals), "high_priority": sum(1 for s in all_signals if collector.should_prioritize(s))}


@shared_task(name="execute_technical_mission")
def execute_technical_mission():
    """
    Executa a Missão Técnica (Google Search, Maps).
    Periodicidade sugerida: A cada 6 horas.
    """
    logger.info("🔍 Iniciando Missão Técnica...")
    
    collector = SignalsCollector()
    google_scraper = GoogleScraper()
    
    # Configuração
    keywords = os.getenv("TECHNICAL_GOOGLE_KEYWORDS", "melhor clínica ultraformer jardins").split(",")
    
    all_signals = []
    
    for keyword in keywords:
        keyword = keyword.strip()
        logger.info(f"Buscando: '{keyword}'...")
        
        results = google_scraper.search_google(
            query=keyword,
            location="São Paulo, Brazil",
            num_results=10
        )
        
        for result_data in results:
            signal = Signal(
                source=result_data["source"],
                content=result_data["content"],
                author_handle="google_user",  # Anônimo
                url=result_data["url"],
                intent_layer=IntentLayer.DIRECT,  # Busca ativa = intenção direta
                mission_type="technical",
                geo_context="São Paulo",
                luxury_indicators=[],
                timestamp=result_data.get("timestamp", "")
            )
            
            all_signals.append(signal)
    
    logger.info(f"✅ Missão Técnica concluída: {len(all_signals)} sinais capturados")
    
    return {"signals_captured": len(all_signals)}


@shared_task(name="execute_luxury_mission")
def execute_luxury_mission():
    """
    Executa a Missão Luxo (Casa Vogue, Forbes Life).
    Periodicidade sugerida: A cada 24 horas.
    """
    logger.info("💎 Iniciando Missão Luxo...")
    
    collector = SignalsCollector()
    luxury_scraper = LuxuryMediaScraper()
    
    all_signals = []
    
    # Casa Vogue
    logger.info("Scraping Casa Vogue...")
    vogue_articles = luxury_scraper.scrape_casa_vogue(
        keywords=["rejuvenescimento", "protocolo", "estética", "preparação"],
        max_articles=10
    )
    
    for article_data in vogue_articles:
        signal = Signal(
            source=article_data["source"],
            content=article_data["content"],
            author_handle="casa_vogue",
            url=article_data["url"],
            intent_layer=IntentLayer.LIFESTYLE,
            mission_type="luxury",
            geo_context=None,
            luxury_indicators=collector.detect_luxury_indicators(article_data["content"]),
            timestamp=article_data["timestamp"]
        )
        
        all_signals.append(signal)
    
    # Forbes Life
    logger.info("Scraping Forbes Life...")
    forbes_articles = luxury_scraper.scrape_forbes_life(
        keywords=["luxo", "estética", "bem-estar"],
        max_articles=10
    )
    
    for article_data in forbes_articles:
        signal = Signal(
            source=article_data["source"],
            content=article_data["content"],
            author_handle="forbes_life",
            url=article_data["url"],
            intent_layer=IntentLayer.LIFESTYLE,
            mission_type="luxury",
            geo_context=None,
            luxury_indicators=collector.detect_luxury_indicators(article_data["content"]),
            timestamp=article_data["timestamp"]
        )
        
        all_signals.append(signal)
    
    logger.info(f"✅ Missão Luxo concluída: {len(all_signals)} sinais capturados")
    
    return {"signals_captured": len(all_signals)}
