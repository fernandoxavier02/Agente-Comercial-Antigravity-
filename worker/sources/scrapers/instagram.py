"""
Instagram Scraper usando Instaloader
Captura comentários de perfis estratégicos (tecnologias, concorrentes)
"""

import instaloader
from typing import List, Dict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class InstagramScraper:
    """
    Scraper de Instagram focado em comentários de posts recentes.
    Usa Instaloader (não requer API oficial).
    """
    
    def __init__(self, session_file: str = None):
        self.loader = instaloader.Instaloader()
        
        # Carregar sessão salva (evita rate limits)
        if session_file:
            try:
                self.loader.load_session_from_file(session_file)
                logger.info(f"Sessão carregada de {session_file}")
            except Exception as e:
                logger.warning(f"Não foi possível carregar sessão: {e}")
    
    def scrape_profile_comments(
        self, 
        profile_username: str, 
        max_posts: int = 10,
        days_back: int = 7,
        keywords: List[str] = None
    ) -> List[Dict]:
        """
        Scrape comentários de posts recentes de um perfil.
        
        Args:
            profile_username: Username do perfil (ex: "merz_aesthetics")
            max_posts: Número máximo de posts para analisar
            days_back: Quantos dias atrás buscar
            keywords: Filtrar comentários que contenham essas palavras
        
        Returns:
            Lista de dicionários com dados dos comentários
        """
        signals = []
        
        try:
            profile = instaloader.Profile.from_username(
                self.loader.context, 
                profile_username
            )
            
            cutoff_date = datetime.now() - timedelta(days=days_back)
            posts_analyzed = 0
            
            logger.info(f"Analisando perfil @{profile_username}...")
            
            for post in profile.get_posts():
                # Limitar por data
                if post.date < cutoff_date:
                    break
                
                # Limitar número de posts
                if posts_analyzed >= max_posts:
                    break
                
                posts_analyzed += 1
                
                # Analisar comentários do post
                for comment in post.get_comments():
                    comment_text = comment.text.lower()
                    
                    # Filtrar por keywords (se fornecidas)
                    if keywords:
                        if not any(kw.lower() in comment_text for kw in keywords):
                            continue
                    
                    signals.append({
                        "source": "instagram_comment",
                        "content": comment.text,
                        "author_handle": f"@{comment.owner.username}",
                        "author_profile_url": f"https://instagram.com/{comment.owner.username}",
                        "post_url": f"https://instagram.com/p/{post.shortcode}",
                        "post_caption": post.caption[:200] if post.caption else "",
                        "timestamp": comment.created_at_utc.isoformat(),
                        "likes": comment.likes_count if hasattr(comment, 'likes_count') else 0,
                        "profile_source": profile_username,
                    })
            
            logger.info(f"Capturados {len(signals)} comentários de @{profile_username}")
            
        except instaloader.exceptions.ProfileNotExistsException:
            logger.error(f"Perfil @{profile_username} não existe")
        except instaloader.exceptions.ConnectionException as e:
            logger.error(f"Erro de conexão ao scraping @{profile_username}: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao scraping @{profile_username}: {e}")
        
        return signals
    
    def scrape_hashtag_posts(
        self, 
        hashtag: str, 
        max_posts: int = 20,
        geo_filter: str = None
    ) -> List[Dict]:
        """
        Scrape posts de uma hashtag específica.
        
        Args:
            hashtag: Hashtag sem # (ex: "harmonizacaofacial")
            max_posts: Número máximo de posts
            geo_filter: Filtrar por localização (ex: "São Paulo")
        
        Returns:
            Lista de posts com metadados
        """
        signals = []
        
        try:
            hashtag_obj = instaloader.Hashtag.from_name(self.loader.context, hashtag)
            posts_analyzed = 0
            
            logger.info(f"Analisando hashtag #{hashtag}...")
            
            for post in hashtag_obj.get_posts():
                if posts_analyzed >= max_posts:
                    break
                
                # Filtro geográfico (se fornecido)
                if geo_filter and post.location:
                    if geo_filter.lower() not in post.location.name.lower():
                        continue
                
                signals.append({
                    "source": "instagram_hashtag",
                    "content": post.caption if post.caption else "",
                    "author_handle": f"@{post.owner_username}",
                    "author_profile_url": f"https://instagram.com/{post.owner_username}",
                    "post_url": f"https://instagram.com/p/{post.shortcode}",
                    "timestamp": post.date_utc.isoformat(),
                    "likes": post.likes,
                    "comments_count": post.comments,
                    "location": post.location.name if post.location else None,
                    "hashtag_source": hashtag,
                })
                
                posts_analyzed += 1
            
            logger.info(f"Capturados {len(signals)} posts de #{hashtag}")
            
        except Exception as e:
            logger.error(f"Erro ao scraping hashtag #{hashtag}: {e}")
        
        return signals

# ===== EXEMPLO DE USO =====
if __name__ == "__main__":
    scraper = InstagramScraper()
    
    # Testar scraping de comentários
    comments = scraper.scrape_profile_comments(
        profile_username="merz_aesthetics",
        max_posts=5,
        keywords=["quero", "fazer", "clínica", "recomendação"]
    )
    
    print(f"Capturados {len(comments)} comentários")
    if comments:
        print(f"Exemplo: {comments[0]}")
