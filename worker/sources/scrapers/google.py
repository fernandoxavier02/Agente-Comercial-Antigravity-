"""
Google Scraper usando SerpAPI
Captura resultados de busca e reviews do Google Maps
"""

from serpapi import GoogleSearch
from typing import List, Dict
import logging
import os

logger = logging.getLogger(__name__)

class GoogleScraper:
    """
    Scraper de Google Search e Google Maps usando SerpAPI.
    Requer API Key (plano gratuito: 100 buscas/mês).
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SERPAPI_KEY")
        if not self.api_key:
            logger.warning("SERPAPI_KEY não configurada. Scraping do Google desabilitado.")
    
    def search_google(
        self, 
        query: str, 
        location: str = "São Paulo, Brazil",
        num_results: int = 10
    ) -> List[Dict]:
        """
        Busca no Google Search.
        
        Args:
            query: Termo de busca (ex: "melhor clínica ultraformer jardins")
            location: Localização da busca
            num_results: Número de resultados
        
        Returns:
            Lista de resultados com título, snippet, URL
        """
        if not self.api_key:
            return []
        
        signals = []
        
        try:
            params = {
                "q": query,
                "location": location,
                "hl": "pt",
                "gl": "br",
                "num": num_results,
                "api_key": self.api_key
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            for result in results.get("organic_results", []):
                signals.append({
                    "source": "google_search",
                    "content": f"{result.get('title', '')} - {result.get('snippet', '')}",
                    "url": result.get("link", ""),
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "position": result.get("position", 0),
                    "query": query,
                })
            
            logger.info(f"Capturados {len(signals)} resultados para '{query}'")
            
        except Exception as e:
            logger.error(f"Erro ao buscar no Google: {e}")
        
        return signals
    
    def search_google_maps(
        self, 
        query: str, 
        location: str = "São Paulo, SP, Brazil"
    ) -> List[Dict]:
        """
        Busca no Google Maps (ex: clínicas concorrentes).
        
        Args:
            query: Nome da clínica ou tipo de negócio
            location: Localização
        
        Returns:
            Lista de estabelecimentos com reviews
        """
        if not self.api_key:
            return []
        
        signals = []
        
        try:
            params = {
                "engine": "google_maps",
                "q": query,
                "ll": "@-23.5505,-46.6333,12z",  # São Paulo coords
                "type": "search",
                "api_key": self.api_key
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            for place in results.get("local_results", []):
                # Capturar reviews se disponíveis
                reviews_data = place.get("reviews", [])
                
                signals.append({
                    "source": "google_maps",
                    "content": f"{place.get('title', '')} - {place.get('description', '')}",
                    "title": place.get("title", ""),
                    "address": place.get("address", ""),
                    "rating": place.get("rating", 0),
                    "reviews_count": place.get("reviews", 0),
                    "url": place.get("link", ""),
                    "query": query,
                })
            
            logger.info(f"Capturados {len(signals)} resultados do Maps para '{query}'")
            
        except Exception as e:
            logger.error(f"Erro ao buscar no Google Maps: {e}")
        
        return signals

# ===== EXEMPLO DE USO =====
if __name__ == "__main__":
    # Requer SERPAPI_KEY no .env
    scraper = GoogleScraper()
    
    # Testar busca
    results = scraper.search_google(
        query="melhor clínica ultraformer jardins são paulo",
        num_results=5
    )
    
    print(f"Capturados {len(results)} resultados")
