"""
Luxury Media Scraper
Captura artigos de sites de lifestyle premium (Casa Vogue, Forbes Life)
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class LuxuryMediaScraper:
    """
    Scraper de sites de luxo e lifestyle.
    Foco: Artigos sobre estética, bem-estar e preparação para eventos.
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_casa_vogue(
        self, 
        keywords: List[str] = None,
        max_articles: int = 10
    ) -> List[Dict]:
        """
        Scrape artigos da Casa Vogue relacionados a estética.
        
        Args:
            keywords: Palavras-chave para filtrar (ex: ["estética", "rejuvenescimento"])
            max_articles: Número máximo de artigos
        
        Returns:
            Lista de artigos com título, snippet, URL
        """
        signals = []
        
        try:
            # URL de busca na Casa Vogue (ajustar conforme estrutura real do site)
            search_url = "https://casavogue.globo.com/busca/?q=estética+facial"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Exemplo de parsing (ajustar seletores CSS conforme site real)
            articles = soup.select('.widget--card', limit=max_articles)
            
            for article in articles:
                title_elem = article.select_one('.widget--card__title')
                link_elem = article.select_one('a')
                snippet_elem = article.select_one('.widget--card__description')
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    url = link_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    # Filtrar por keywords se fornecidas
                    if keywords:
                        content_lower = f"{title} {snippet}".lower()
                        if not any(kw.lower() in content_lower for kw in keywords):
                            continue
                    
                    signals.append({
                        "source": "casa_vogue",
                        "content": f"{title} - {snippet}",
                        "title": title,
                        "snippet": snippet,
                        "url": url if url.startswith('http') else f"https://casavogue.globo.com{url}",
                        "timestamp": datetime.now().isoformat(),
                    })
            
            logger.info(f"Capturados {len(signals)} artigos da Casa Vogue")
            
        except Exception as e:
            logger.error(f"Erro ao scraping Casa Vogue: {e}")
        
        return signals
    
    def scrape_forbes_life(
        self, 
        keywords: List[str] = None,
        max_articles: int = 10
    ) -> List[Dict]:
        """
        Scrape artigos da Forbes Life Brasil.
        
        Args:
            keywords: Palavras-chave para filtrar
            max_articles: Número máximo de artigos
        
        Returns:
            Lista de artigos
        """
        signals = []
        
        try:
            # URL de busca na Forbes (ajustar conforme estrutura real)
            search_url = "https://forbes.com.br/?s=estética+luxo"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Parsing (ajustar seletores conforme site real)
            articles = soup.select('article', limit=max_articles)
            
            for article in articles:
                title_elem = article.select_one('h2, h3')
                link_elem = article.select_one('a')
                snippet_elem = article.select_one('.excerpt, p')
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    url = link_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    if keywords:
                        content_lower = f"{title} {snippet}".lower()
                        if not any(kw.lower() in content_lower for kw in keywords):
                            continue
                    
                    signals.append({
                        "source": "forbes_life",
                        "content": f"{title} - {snippet}",
                        "title": title,
                        "snippet": snippet,
                        "url": url,
                        "timestamp": datetime.now().isoformat(),
                    })
            
            logger.info(f"Capturados {len(signals)} artigos da Forbes Life")
            
        except Exception as e:
            logger.error(f"Erro ao scraping Forbes Life: {e}")
        
        return signals

# ===== EXEMPLO DE USO =====
if __name__ == "__main__":
    scraper = LuxuryMediaScraper()
    
    # Testar scraping
    articles = scraper.scrape_casa_vogue(
        keywords=["rejuvenescimento", "protocolo", "estética"]
    )
    
    print(f"Capturados {len(articles)} artigos")
