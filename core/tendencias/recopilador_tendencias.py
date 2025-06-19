"""
Módulo para la obtención de tendencias de diferentes fuentes.
"""

import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class RecopiladorTendencias:
    """Clase para recopilar tendencias de diversas fuentes."""
    
    def __init__(self):
        """Constructor de la clase RecopiladorTendencias."""
        self.tendencias_cache = {}
    
    def obtener_tendencias_google_trends(self):
        """Scraping de Google Trends para obtener tendencias reales"""
        print("   📈 Obteniendo tendencias de Google Trends...")
        tendencias = []
        
        try:
            # URLs de diferentes categorías de Google Trends
            urls_trends = [
                "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US",
                "https://trends.google.com/trends/trendingsearches/daily/rss?geo=ES",
                "https://trends.google.com/trends/trendingsearches/daily/rss?geo=MX"
            ]
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            for url in urls_trends:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'xml')
                        items = soup.find_all('item')
                        for item in items[:5]:  # Top 5 de cada región
                            title = item.find('title')
                            if title:
                                tendencias.append(title.text.strip())
                except:
                    continue
                    
            # Limpiar y deduplicar
            tendencias = list(set([t for t in tendencias if len(t) > 3 and len(t) < 50]))
            
        except Exception as e:
            print(f"      ⚠️ Error obteniendo Google Trends: {e}")
        
        return tendencias[:20]  # Top 20
    
    def obtener_tendencias_youtube(self):
        """Obtener tendencias de YouTube"""
        print("   🎥 Analizando tendencias de YouTube...")
        tendencias = []
        
        try:
            # Buscar en YouTube trending topics (simulado)
            temas_youtube = [
                "challenge", "reaction", "review", "tutorial", "unboxing",
                "day in my life", "story time", "transformation", "before and after",
                "trying", "testing", "comparison", "tier list", "ranking"
            ]
            
            # Agregar temas populares actuales
            fecha_actual = datetime.now()
            if fecha_actual.month == 12:
                temas_youtube.extend(["christmas", "year recap", "2024 trends", "new year"])
            elif fecha_actual.month == 1:
                temas_youtube.extend(["new year resolutions", "goal setting", "fresh start"])
            
            tendencias.extend(temas_youtube)
            
        except Exception as e:
            print(f"      ⚠️ Error obteniendo tendencias YouTube: {e}")
        
        return tendencias
    
    def obtener_tendencias_tiktok(self):
        """Obtener tendencias de TikTok"""
        print("   📱 Analizando tendencias de TikTok...")
        tendencias = []
        
        try:
            # Tendencias típicas de TikTok
            temas_tiktok = [
                "aesthetic", "that girl", "glow up", "productivity", "study with me",
                "get ready with me", "day in my life", "what I eat", "outfit of the day",
                "mini vlog", "life update", "self care", "wellness", "manifestation"
            ]
            
            tendencias.extend(temas_tiktok)
            
        except Exception as e:
            print(f"      ⚠️ Error obteniendo tendencias TikTok: {e}")
        
        return tendencias
    
    def obtener_tendencias_news(self):
        """Obtener noticias y eventos actuales"""
        print("   📰 Obteniendo noticias actuales...")
        tendencias = []
        
        try:
            # Fuentes de noticias
            urls_news = [
                "https://feeds.bbci.co.uk/news/technology/rss.xml",
                "https://rss.cnn.com/rss/edition.rss"
            ]
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            for url in urls_news:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'xml')
                        items = soup.find_all('item')
                        for item in items[:3]:
                            title = item.find('title')
                            if title:
                                # Extraer palabras clave del título
                                palabras = title.text.split()
                                for palabra in palabras:
                                    if len(palabra) > 4 and palabra.isalpha():
                                        tendencias.append(palabra.lower())
                except:
                    continue
                    
        except Exception as e:
            print(f"      ⚠️ Error obteniendo noticias: {e}")
        
        return list(set(tendencias))[:15]
    
    def obtener_todas_las_tendencias(self):
        """Obtener tendencias de múltiples fuentes simultáneamente"""
        print("🔍 Recopilando tendencias de múltiples fuentes...")
        
        # Tendencias base siempre disponibles
        tendencias_base = [
            "artificial intelligence", "productivity tips", "morning routine",
            "healthy recipes", "workout routine", "study tips", "life hacks",
            "tech review", "fashion trends", "travel tips", "money saving",
            "career advice", "relationship tips", "mental health", "self care"
        ]
        
        todas_tendencias = tendencias_base.copy()
        
        # Ejecutar scraping en paralelo
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self.obtener_tendencias_google_trends),
                executor.submit(self.obtener_tendencias_youtube),
                executor.submit(self.obtener_tendencias_tiktok),
                executor.submit(self.obtener_tendencias_news)
            ]
            
            for future in futures:
                try:
                    result = future.result(timeout=15)
                    if result:
                        todas_tendencias.extend(result)
                except:
                    continue
        
        # Limpiar y procesar tendencias
        tendencias_limpias = []
        for tendencia in todas_tendencias:
            if isinstance(tendencia, str) and 3 <= len(tendencia) <= 50:
                tendencia_limpia = re.sub(r'[^\w\s]', '', tendencia.lower()).strip()
                if tendencia_limpia and tendencia_limpia not in tendencias_limpias:
                    tendencias_limpias.append(tendencia_limpia)
        
        print(f"   ✅ Recopiladas {len(tendencias_limpias)} tendencias únicas")
        return tendencias_limpias[:50]  # Top 50 tendencias
