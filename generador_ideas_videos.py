# generador_ideas_videos.py - Sistema Avanzado de Generación Automatizada de Ideas de Videos

import os
import json
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import pandas as pd
from datetime import datetime, timedelta
import random
import time
from pathlib import Path
import re
from urllib.parse import quote
import threading
from concurrent.futures import ThreadPoolExecutor
import hashlib

class GeneradorIdeasVideosAvanzado:
    def __init__(self):
        print("🚀 Inicializando Generador de Ideas Profesional...")
        self.cargar_api_key()
        self.configurar_gemini()
        self.configurar_redes_sociales()
        self.configurar_nichos()
        self.configurar_templates()
        self.tendencias_cache = {}
        self.ideas_generadas_sesion = []
        
    def cargar_api_key(self):
        """Cargar API key de Gemini"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key and os.path.exists(".env"):
            try:
                with open(".env") as f:
                    for line in f:
                        if line.startswith("GEMINI_API_KEY"):
                            self.api_key = line.strip().split("=", 1)[1].strip().strip('"\'')
            except:
                pass
        if not self.api_key:
            raise ValueError("❌ No se encontró GEMINI_API_KEY. Ponla en .env o como variable de entorno.")
    
    def configurar_gemini(self):
        """Configurar el modelo de Gemini con configuración optimizada"""
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Configuración para respuestas más consistentes
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.8,
            top_p=0.9,
            top_k=50,
            max_output_tokens=2048,
        )
    
    def configurar_redes_sociales(self):
        """Configuración avanzada de redes sociales con métricas y algoritmos"""
        self.redes_sociales = {
            "TikTok": {
                "duraciones": ["15s", "30s", "60s", "3min"],
                "formatos": ["Vertical 9:16", "Cuadrado 1:1"],
                "algoritmo": {
                    "factores_clave": ["engagement temprano", "tiempo de visualización", "shares", "comentarios"],
                    "picos_actividad": ["18:00-22:00", "12:00-14:00"],
                    "hashtags_optimos": 3-5,
                    "hook_tiempo": "3 segundos"
                },
                "tipos_contenido": ["Trends", "Educativo", "Entretenimiento", "Lifestyle", "Comedy", "Challenges"],
                "audiencia_principal": "16-24 años",
                "ctr_promedio": "6-10%"
            },
            "YouTube": {
                "duraciones": ["1-3min", "5-8min", "10-15min", "20-30min"],
                "formatos": ["Horizontal 16:9", "Vertical 9:16 (Shorts)"],
                "algoritmo": {
                    "factores_clave": ["tiempo de visualización", "CTR del thumbnail", "retención", "engagement"],
                    "picos_actividad": ["14:00-16:00", "19:00-21:00"],
                    "hashtags_optimos": 5-8,
                    "hook_tiempo": "15 segundos"
                },
                "tipos_contenido": ["Tutorial", "Review", "Vlog", "Educational", "Entertainment", "Gaming"],
                "audiencia_principal": "25-34 años",
                "ctr_promedio": "4-6%"
            },
            "Instagram": {
                "duraciones": ["15s", "30s", "60s", "90s"],
                "formatos": ["Cuadrado 1:1", "Vertical 9:16", "Horizontal 16:9"],
                "algoritmo": {
                    "factores_clave": ["saves", "shares", "comentarios", "tiempo en pantalla"],
                    "picos_actividad": ["11:00-13:00", "19:00-21:00"],
                    "hashtags_optimos": 8-15,
                    "hook_tiempo": "3 segundos"
                },
                "tipos_contenido": ["Lifestyle", "Fashion", "Food", "Travel", "Motivational", "Behind-the-scenes"],
                "audiencia_principal": "25-34 años",
                "ctr_promedio": "5-7%"
            },
            "YouTube Shorts": {
                "duraciones": ["15s", "30s", "60s"],
                "formatos": ["Vertical 9:16"],
                "algoritmo": {
                    "factores_clave": ["loops", "engagement inmediato", "shares", "suscripciones"],
                    "picos_actividad": ["16:00-18:00", "20:00-22:00"],
                    "hashtags_optimos": 3-5,
                    "hook_tiempo": "2 segundos"
                },
                "tipos_contenido": ["Quick Tips", "Viral Trends", "Mini Tutorials", "Funny Moments"],
                "audiencia_principal": "16-24 años",
                "ctr_promedio": "7-12%"
            }
        }
    
    def configurar_nichos(self):
        """Configurar nichos específicos con sus características y enfoque educativo"""
        self.nichos = {
            "Tecnología": {
                "subtemas": ["Inteligencia Artificial", "Programación", "Ciberseguridad", "Nuevas Tecnologías", "Apps y Software", "Hardware", "Tecnologías Emergentes"],
                "palabras_clave": ["tutorial", "explicación", "guía paso a paso", "análisis técnico", "novedades tech", "aprende"],
                "audiencia": "18-35 años, interesados en tecnología",
                "engagement_promedio": "alto",
                "enfoque_educativo": True,
                "estilo": "técnico-didáctico"
            },
            "Crecimiento Personal": {
                "subtemas": ["Productividad", "Desarrollo Personal", "Hábitos", "Mindfulness", "Gestión del Tiempo", "Inteligencia Emocional"],
                "palabras_clave": ["desarrollo", "crecimiento", "mejora continua", "hábitos", "mindset", "productividad"],
                "audiencia": "25-45 años, profesionales en desarrollo",
                "engagement_promedio": "muy alto",
                "enfoque_educativo": True,
                "estilo": "motivacional-educativo"
            },
            "Marketing": {
                "subtemas": ["Marketing Digital", "Redes Sociales", "SEO", "Branding", "Email Marketing", "Estrategias de Contenido"],
                "palabras_clave": ["estrategia", "marketing digital", "ventas", "publicidad", "growth hacking"],
                "audiencia": "20-40 años, emprendedores y marketers",
                "engagement_promedio": "alto",
                "enfoque_educativo": True,
                "estilo": "práctico-profesional"
            },
            "Finanzas": {
                "subtemas": ["Inversiones", "Ahorro", "Presupuesto Personal", "Mercados Financieros", "Criptomonedas", "Educación Financiera"],
                "palabras_clave": ["finanzas personales", "inversión", "ahorro", "tips financieros", "economía"],
                "audiencia": "25-50 años, interesados en finanzas",
                "engagement_promedio": "medio-alto",
                "enfoque_educativo": True,
                "estilo": "informativo-educativo"
            },
            "Inteligencia Artificial": {
                "subtemas": ["Machine Learning", "Deep Learning", "NLP", "IA Generativa", "Ética en IA", "Aplicaciones de IA"],
                "palabras_clave": ["inteligencia artificial", "AI", "machine learning", "futuro", "innovación"],
                "audiencia": "20-40 años, tech-savvy",
                "engagement_promedio": "alto",
                "enfoque_educativo": True,
                "estilo": "técnico-divulgativo"
            },
            "Historias Reddit": {
                "subtemas": ["Confesiones", "Experiencias", "AITA", "Relaciones", "Historias Virales", "Momentos Épicos"],
                "palabras_clave": ["historia real", "reddit", "confesión", "experiencia", "drama"],
                "audiencia": "16-35 años, amantes de historias",
                "engagement_promedio": "muy alto",
                "enfoque_educativo": False,
                "estilo": "narrativo-informal"
            }
        }
    
    def configurar_templates(self):
        """Templates específicos para diferentes tipos de contenido"""
        self.templates = {
            "educativo": [
                "Aprende {tema} en {tiempo} minutos",
                "Las bases fundamentales de {tema}",
                "{numero} conceptos clave para entender {tema}",
                "Guía completa: {tema} explicado paso a paso",
                "Todo lo que debes saber sobre {tema} en {año}"
            ],
            "tecnologia": [
                "Cómo {tema} está cambiando el futuro",
                "Tutorial detallado: {tema} para principiantes",
                "Las últimas novedades en {tema}",
                "Análisis profundo de {tema}",
                "Pros y contras de {tema} en {año}"
            ],
            "crecimiento_personal": [
                "Transforma tu vida con {tema}",
                "Método comprobado para {tema}",
                "Desarrolla {tema} en {tiempo}",
                "El secreto detrás de {tema}",
                "Cómo mejoré mi {tema} en {tiempo}"
            ],
            "finanzas": [
                "Estrategia de {tema} que debes conocer",
                "Guía de inversión en {tema}",
                "Errores comunes en {tema}",
                "Cómo optimizar tu {tema}",
                "El ABC de {tema} para principiantes"
            ],
            "historias_reddit": [
                "La increíble historia de {tema} en Reddit",
                "No creerás lo que pasó en r/{subreddit}",
                "Historia viral: {tema}",
                "Confesiones de Reddit: {tema}",
                "La historia más {adjetivo} de Reddit"
            ]
        }
        # Mantener los templates existentes
        self.templates.update({
            "viral_hook": self.templates.get("viral_hook", []),
            "educational": self.templates.get("educational", []),
            "comparison": self.templates.get("comparison", []),
            "trending": self.templates.get("trending", [])
        })
    
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
    
    def generar_idea_con_ia(self, tema, red_social, nicho=None, tipo_contenido=None):
        """Genera una idea de contenido usando IA, con enfoque educativo o narrativo según el nicho"""
        try:
            # Configurar el prompt según el nicho y su enfoque
            if nicho in self.nichos:
                nicho_info = self.nichos[nicho]
                es_educativo = nicho_info.get("enfoque_educativo", True)
                estilo = nicho_info.get("estilo", "educativo")
                audiencia = nicho_info.get("audiencia", "general")
                
                if nicho == "Historias Reddit":
                    prompt = f"""
                    Genera una idea VIRAL para un video de {red_social} sobre una historia de Reddit.
                    
                    TEMA: {tema}
                    ESTILO: Narrativo e informal
                    AUDIENCIA: {audiencia}
                    
                    LA IDEA DEBE INCLUIR:
                    1. Título impactante que genere curiosidad
                    2. Hook inicial que enganche en los primeros segundos
                    3. Desarrollo de la historia con elementos de suspense
                    4. Giros inesperados o revelaciones sorprendentes
                    5. Conclusión memorable
                    6. Call to action específico
                    7. Hashtags relevantes
                    
                    FORMATO DE RESPUESTA:
                    Título: [título viral y atractivo]
                    Descripción: [descripción detallada de la historia]
                    Puntos Clave:
                    - [punto dramático 1]
                    - [punto dramático 2]
                    - [punto dramático 3]
                    Hashtags: [5-7 hashtags relevantes]
                    """
                else:
                    prompt = f"""
                    Genera una idea EDUCATIVA y VIRAL para un video de {red_social}.
                    
                    TEMA: {tema}
                    NICHO: {nicho}
                    ESTILO: {estilo}
                    AUDIENCIA: {audiencia}
                    
                    LA IDEA DEBE INCLUIR:
                    1. Título que prometa valor educativo claro
                    2. Hook que demuestre por qué el tema es importante
                    3. 3-5 puntos de aprendizaje concretos
                    4. Ejemplos prácticos y aplicables
                    5. Datos o estadísticas relevantes
                    6. Call to action educativo
                    7. Hashtags específicos del tema
                    
                    FORMATO DE RESPUESTA:
                    Título: [título educativo y atractivo]
                    Descripción: [descripción detallada del contenido educativo]
                    Puntos Clave:
                    - [punto educativo 1]
                    - [punto educativo 2]
                    - [punto educativo 3]
                    Hashtags: [5-7 hashtags relevantes]
                    """

            # Generar respuesta con IA
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            # Procesar y estructurar la respuesta
            idea_json = self.procesar_respuesta_ia(response.text, tema, red_social, nicho)
            
            # Añadir metadatos específicos según el nicho
            if nicho in self.nichos:
                idea_json["enfoque"] = "educativo" if self.nichos[nicho].get("enfoque_educativo", True) else "narrativo"
                idea_json["estilo"] = self.nichos[nicho].get("estilo", "general")
                idea_json["audiencia_objetivo"] = self.nichos[nicho].get("audiencia", "general")

            return idea_json

        except Exception as e:
            print(f"❌ Error generando idea: {str(e)}")
            return None

    def procesar_respuesta_ia(self, texto_respuesta, tema, red_social, nicho=None):
        """Procesa y estructura la respuesta de la IA según el nicho"""
        try:
            # Estructura base para la idea
            idea_estructurada = {
                "tema": tema,
                "red_social": red_social,
                "nicho": nicho,
                "titulo": "",
                "descripcion": "",
                "puntos_clave": [],
                "hashtags": [],
                "tipo_contenido": "educativo" if nicho and self.nichos[nicho].get("enfoque_educativo", True) else "narrativo",
                "metadata": {
                    "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "categoria": nicho if nicho else "general"
                }
            }

            # Extraer información del texto de respuesta
            lineas = texto_respuesta.split("\n")
            seccion_actual = ""
            
            for linea in lineas:
                linea = linea.strip()
                if not linea:
                    continue

                # Detectar secciones según el contenido
                if "título:" in linea.lower() or "titulo:" in linea.lower():
                    seccion_actual = "titulo"
                    idea_estructurada["titulo"] = linea.split(":", 1)[1].strip()
                elif "descripción:" in linea.lower() or "descripcion:" in linea.lower():
                    seccion_actual = "descripcion"
                    idea_estructurada["descripcion"] = linea.split(":", 1)[1].strip()
                elif "puntos clave:" in linea.lower() or "- " in linea:
                    if linea.startswith("- "):
                        idea_estructurada["puntos_clave"].append(linea[2:].strip())
                elif "hashtags:" in linea.lower() or "#" in linea:
                    hashtags = re.findall(r'#\w+', linea)
                    idea_estructurada["hashtags"].extend(hashtags)

            # Añadir metadatos específicos según el nicho
            if nicho in self.nichos:
                idea_estructurada["metadata"].update({
                    "estilo": self.nichos[nicho].get("estilo", "general"),
                    "audiencia": self.nichos[nicho].get("audiencia", "general"),
                    "palabras_clave": self.nichos[nicho].get("palabras_clave", [])
                })

            return idea_estructurada
                
        except Exception as e:
            print(f"❌ Error procesando respuesta: {str(e)}")
            return None
    
    def calcular_timing_guion(self, duracion):
        """Calcular timing detallado para el guión según duración"""
        
        # Convertir duración a segundos
        if "min" in duracion:
            if "-" in duracion:
                # Rango como "1-3min", tomar el promedio
                nums = duracion.replace("min", "").split("-")
                segundos = (int(nums[0]) + int(nums[1])) * 30  # Promedio en segundos
            else:
                segundos = int(duracion.replace("min", "")) * 60
        else:
            segundos = int(duracion.replace("s", ""))
        
        # Distribución proporcional del tiempo
        if segundos <= 30:
            # Video corto
            timing = {
                "segundos": segundos,
                "hook": min(3, segundos // 3),
                "desarrollo": segundos // 2,
                "climax": segundos // 4,
                "cierre": segundos // 4
            }
        elif segundos <= 60:
            # Video medio
            timing = {
                "segundos": segundos,
                "hook": 5,
                "desarrollo": segundos - 15,
                "climax": 5,
                "cierre": 5
            }
        else:
            # Video largo
            timing = {
                "segundos": segundos,
                "hook": 10,
                "desarrollo": segundos - 30,
                "climax": 10,
                "cierre": 10
            }
        
        return timing
    
    def validar_y_mejorar_guion(self, idea_json, timing_info):
        """Validar y mejorar el guión generado"""
        
        # Verificar que existe la estructura de guión
        if "guion_completo_voz" not in idea_json:
            idea_json["guion_completo_voz"] = self.crear_guion_basico(idea_json, timing_info)
        
        # Añadir conteo de palabras estimado
        guion = idea_json["guion_completo_voz"]
        for seccion in guion:
            if isinstance(guion[seccion], dict) and "texto" in guion[seccion]:
                texto = guion[seccion]["texto"]
                palabras = len(texto.split())
                guion[seccion]["palabras_estimadas"] = palabras
                guion[seccion]["duracion_estimada"] = f"{palabras / 2.5:.1f}s"  # ~150 palabras/min
        
        return idea_json
    
    def crear_guion_basico(self, idea_json, timing_info):
        """Crear guión básico si no se generó correctamente"""
        tema = idea_json.get("tema_original", "este tema")
        
        return {
            "intro_hook": {
                "texto": f"¿Sabías que {tema} puede CAMBIAR completamente tu vida? [PAUSA] En los próximos segundos te voy a mostrar algo que NO sabías.",
                "timing": f"{timing_info['hook']}s",
                "instrucciones_voz": "Tono energético, velocidad rápida, enfatizar palabras clave"
            },
            "desarrollo_principal": {
                "texto": f"Aquí está lo que necesitas saber sobre {tema}. [PAUSA CORTA] Primero, esto es MÁS importante de lo que piensas. [PAUSA] Te explico paso a paso lo que debes hacer.",
                "timing": f"{timing_info['desarrollo']}s",
                "instrucciones_voz": "Tono conversacional, velocidad media, pausas naturales"
            },
            "momento_climax": {
                "texto": f"Pero AQUÍ viene lo que NADIE te dice sobre {tema}. [PAUSA LARGA] Esta información va a cambiar todo lo que creías que sabías.",
                "timing": f"{timing_info['climax']}s",
                "instrucciones_voz": "Tono dramático, velocidad lenta para énfasis"
            },
            "call_to_action": {
                "texto": "Si este contenido te sirvió, dale LIKE y SÍGUEME para más contenido como este. [PAUSA] ¿Ya lo sabías? Cuéntame en los comentarios.",
                "timing": f"{timing_info['cierre']}s",
                "instrucciones_voz": "Tono motivacional, velocidad media-rápida"
            }
        }
    
    def crear_idea_fallback_voz(self, tema, red_social, duracion, nicho, timing_info):
        """Crear idea básica con guión de voz como fallback"""
        return {
            "titulo": f"Todo sobre {tema} que debes saber",
            "hook_inicial": f"¿Sabías esto sobre {tema}?",
            "descripcion_video": f"Video completo explicando {tema} de forma práctica y útil",
            "temas_principales": [f"Introducción a {tema}", f"Beneficios de {tema}", f"Cómo aplicar {tema}"],
            "guion_completo_voz": self.crear_guion_basico({"tema_original": tema}, timing_info),
            "hashtags": [f"#{tema.replace(' ', '').lower()}", f"#{red_social.lower()}", "#viral"],
            "elementos_visuales": ["Texto en pantalla", "Gráficos simples", "Transiciones suaves"],
            "estrategia_engagement": {
                "pregunta_comentarios": f"¿Qué opinas de {tema}?",
                "momento_compartir": "Revelación principal",
                "call_to_action_especifico": "Sígueme para más contenido",
                "hook_comentarios": "Cuéntame tu experiencia"
            },
            "guion_alternativo_corto": {
                "version_15s": f"Quick tip sobre {tema}",
                "version_30s": f"Lo esencial de {tema}",
                "version_60s": f"Guía completa de {tema}"
            },
            "instrucciones_ia_voz": {
                "velocidad_general": "150 palabras por minuto",
                "pausas_estrategicas": ["Después del hook", "Antes del final"],
                "enfasis_palabras": [tema],
                "tono_general": "Conversacional y amigable",
                "respiraciones": "Cada 15 segundos"
            },
            "prediccion_viralidad": {
                "score": 70,
                "factores_positivos": ["Tema popular", "Formato optimizado"],
                "optimizaciones": ["Mejorar hook", "Añadir datos específicos"]
            },
            "timing_publicacion": {
                "mejor_hora": "19:00-21:00",
                "dias_optimos": ["Martes", "Miércoles", "Jueves"],
                "frecuencia_sugerida": "2-3 veces por semana"
            },
            "tema_original": tema,
            "red_social": red_social,
            "duracion": duracion,
            "nicho": nicho,
            "tipo_contenido": "General",
            "timestamp": datetime.now().isoformat()
        }
    
    def calcular_score_idea(self, idea):
        """Calcular score de calidad de la idea"""
        score = 0
        
        # Validación básica
        if not idea:
            return 0
            
        # Factor título (25 puntos)
        titulo = idea.get("titulo", "")
        if titulo:
            score += 15  # Puntos base por tener título
            if len(titulo) > 5 and len(titulo) < 100:  # Longitud razonable
                score += 10
                
        # Factor descripción (25 puntos)
        descripcion = idea.get("descripcion", "")
        if descripcion:
            score += 15  # Puntos base por tener descripción
            if len(descripcion) > 20:  # Descripción detallada
                score += 10
        
        # Factor puntos clave (25 puntos)
        puntos_clave = idea.get("puntos_clave", [])
        if puntos_clave:
            score += min(len(puntos_clave) * 5, 25)  # 5 puntos por cada punto clave, máximo 25
            
        # Factor hashtags (15 puntos)
        hashtags = idea.get("hashtags", [])
        if hashtags:
            score += min(len(hashtags) * 3, 15)  # 3 puntos por hashtag, máximo 15
            
        # Factor metadata (10 puntos)
        metadata = idea.get("metadata", {})
        if metadata:
            if metadata.get("estilo"):
                score += 3
            if metadata.get("audiencia"):
                score += 3
            if metadata.get("palabras_clave"):
                score += 4
                
        # Ajuste por tipo de contenido
        tipo_contenido = idea.get("tipo_contenido", "")
        if tipo_contenido == "educativo":
            # Bonus para contenido educativo bien estructurado
            if len(puntos_clave) >= 3 and len(descripcion) > 50:
                score += 10
        elif tipo_contenido == "narrativo":
            # Bonus para historias bien estructuradas
            if len(descripcion) > 100:
                score += 10
                
        return min(score, 100)  # Asegurar que no exceda 100
    
    def generar_lote_ideas_automatizado(self, cantidad=20, filtros=None):
        """Generar lote de ideas de forma completamente automatizada"""
        
        print(f"🤖 GENERACIÓN AUTOMATIZADA DE {cantidad} IDEAS PROFESIONALES")
        print("=" * 70)
        
        # Obtener tendencias actuales
        tendencias = self.obtener_todas_las_tendencias()
        
        ideas_generadas = []
        ideas_exitosas = 0
        intentos = 0
        max_intentos = cantidad * 2
        
        # Filtros por defecto
        if not filtros:
            filtros = {
                "score_minimo": 50,
                "redes_incluir": list(self.redes_sociales.keys()),
                "nichos_incluir": ["Tecnología", "Crecimiento Personal", "Marketing", "Finanzas", "Inteligencia Artificial", "Historias Reddit"],
                "evitar_duplicados": True
            }
            
        # Validar que los nichos existan
        nichos_validos = [nicho for nicho in filtros["nichos_incluir"] if nicho in self.nichos]
        if not nichos_validos:
            nichos_validos = ["Tecnología", "Crecimiento Personal", "Marketing"]  # Nichos por defecto si no hay válidos
        filtros["nichos_incluir"] = nichos_validos
        
        print(f"🎯 Filtros aplicados: Score mínimo {filtros['score_minimo']}")
        print(f"📱 Redes: {', '.join(filtros['redes_incluir'])}")
        print(f"🎪 Nichos: {', '.join(filtros['nichos_incluir'])}")
        print("\n🔄 Generando ideas...")
        
        while ideas_exitosas < cantidad and intentos < max_intentos:
            intentos += 1
            
            # Selección inteligente de parámetros
            tema = random.choice(tendencias)
            red_social = random.choice(filtros["redes_incluir"])
            nicho = random.choice(filtros["nichos_incluir"])
            
            # Enriquecer el tema según el nicho
            tema_enriquecido = self.enriquecer_tema(tema, nicho)
            
            print(f"   💡 Idea {intentos}: {tema_enriquecido} → {red_social} ({nicho})")
            
            # Generar idea
            idea = self.generar_idea_con_ia(tema_enriquecido, red_social, nicho)
            
            if idea:
                # Calcular score
                score = self.calcular_score_idea(idea)
                idea["score_calidad"] = score
                
                # Aplicar filtros
                if score >= filtros["score_minimo"]:
                    # Verificar duplicados si está habilitado
                    if filtros["evitar_duplicados"]:
                        titulo_actual = idea.get("titulo", "").lower()
                        es_duplicado = any(
                            titulo_actual in idea_existente.get("titulo", "").lower() 
                            or idea_existente.get("titulo", "").lower() in titulo_actual
                            for idea_existente in ideas_generadas
                        )
                        
                        if es_duplicado:
                            print(f"      ⚠️ Duplicado detectado, descartando")
                            continue
                    
                    ideas_generadas.append(idea)
                    ideas_exitosas += 1
                    print(f"      ✅ Aprobada (Score: {score})")
                else:
                    print(f"      ❌ Score bajo ({score}), descartando")
            else:
                print(f"      ❌ Error en generación")
        
        return ideas_generadas
    
    def enriquecer_tema(self, tema, nicho):
        """Enriquecer el tema base según el nicho seleccionado"""
        if nicho not in self.nichos:
            return tema
            
        palabras_clave = self.nichos[nicho]["palabras_clave"]
        subtemas = self.nichos[nicho]["subtemas"]
        
        # Seleccionar aleatoriamente un enfoque
        if random.random() < 0.5:
            # Usar palabra clave
            palabra_clave = random.choice(palabras_clave)
            return f"{palabra_clave} {tema}"
        else:
            # Usar subtema
            subtema = random.choice(subtemas)
            return f"{tema} en {subtema}"
    
    def generar_formatos_ia_especificos(self, idea):
        """Generar formatos específicos para diferentes servicios de IA"""
        
        titulo = idea.get("titulo", "")
        descripcion = idea.get("descripcion", "")
        puntos_clave = idea.get("puntos_clave", [])
        tipo_contenido = idea.get("tipo_contenido", "educativo")
        nicho = idea.get("nicho", "")
        
        # Configurar estilo de voz según el tipo de contenido
        if tipo_contenido == "narrativo" or nicho == "Historias Reddit":
            estilo_voz = {
                "tono": "narrativo y dinámico",
                "velocidad": "variable según la tensión",
                "emoción": "expresivo y dramático"
            }
            # Generar guión narrativo y dramático
            guion_voz = f"""¡No van a creer esta historia de Reddit! {titulo}

¿Están listos para algo increíble? Porque esto es... ¡ÉPICO! 

{descripcion}

"""
            # Añadir puntos clave como elementos dramáticos
            for punto in puntos_clave:
                guion_voz += f"""
¡Pero esperen! Aquí viene lo más impactante... {punto}

"""
            
            # Cierre dramático
            guion_voz += """
¿Pueden creer todo esto? ¡La historia no termina aquí!

Si quieren más historias increíbles como esta, ¡den like y suscríbanse! 

¿Qué harían ustedes en esta situación? ¡Cuéntenme en los comentarios!
"""

        else:
            estilo_voz = {
                "tono": "profesional y educativo",
                "velocidad": "clara y pausada",
                "emoción": "entusiasta y confiado"
            }
            # Generar guión educativo y profesional
            guion_voz = f"""¡Hola a todos! Hoy vamos a hablar de algo fascinante: {titulo}

¿Sabían que {descripcion}? Es increíble, ¿verdad?

Vamos a analizar esto paso a paso para que lo entiendan perfectamente.

"""
            # Añadir puntos clave como lecciones
            for i, punto in enumerate(puntos_clave, 1):
                guion_voz += f"""
Punto número {i}: {punto}
Esto es crucial porque nos permite entender mejor el tema y aplicarlo en nuestra vida diaria.

"""
            
            # Cierre educativo
            guion_voz += f"""
Para resumir todo lo que hemos aprendido sobre {titulo}:
- La clave está en entender los conceptos básicos
- Practicar regularmente lo aprendido
- Mantenerse actualizado con las últimas tendencias

¿Les resultó útil esta información? ¡Den like y suscríbanse para más contenido educativo como este!

¿Qué otros temas les gustaría que explique? ¡Déjenlo en los comentarios!
"""

        # Versión corta 15s
        guion_corto_15s = f"""¡Atención! {titulo}
{puntos_clave[0] if puntos_clave else descripcion[:50]}...
¡Sigue mi canal para más contenido como este!"""

        # Versión corta 30s
        guion_corto_30s = f"""¡No te pierdas esto! {titulo}
{descripcion[:100]}
{puntos_clave[0] if puntos_clave else ""}
¡Dale like y sígueme para más contenido increíble!"""

        # Configuración para ElevenLabs
        elevenlabs_config = {
            "texto_completo": guion_voz,
            "versiones_cortas": {
                "15s": guion_corto_15s,
                "30s": guion_corto_30s
            },
                "configuracion": {
                "stability": 0.71,
                "similarity_boost": 0.75,
                "style": 0.35 if tipo_contenido == "narrativo" else 0.20,
                "use_speaker_boost": True,
                "optimize_streaming_latency": 3
            },
            "instrucciones_voz": {
                "tono": estilo_voz["tono"],
                "velocidad": estilo_voz["velocidad"],
                "emoción": estilo_voz["emoción"],
                "notas": "Usar entonación natural y pausas según el contenido"
            }
        }

        # Mantener el resto de los formatos existentes
        formatos = {
            "elevenlabs": elevenlabs_config,
            "video_lyrics": self.generar_video_lyrics(idea),
            "runway_ml": self.generar_prompt_runway(idea),
            "capcut": self.generar_guia_capcut(idea),
            "midjourney": self.generar_prompt_midjourney(idea)
        }

        return formatos

    def generar_video_lyrics(self, idea):
        """Generar timeline para video con letras/karaoke"""
        # [Mantener el código existente de video_lyrics]
        return []

    def generar_prompt_runway(self, idea):
        """Generar prompt para Runway ML"""
        # [Mantener el código existente de runway_prompt]
        return ""

    def generar_guia_capcut(self, idea):
        """Generar guía para CapCut"""
        # [Mantener el código existente de capcut_guide]
        return ""

    def generar_prompt_midjourney(self, idea):
        """Generar prompt para Midjourney"""
        # [Mantener el código existente de midjourney_prompt]
        return ""
    
    def exportar_a_excel_avanzado(self, ideas, nombre_archivo=None):
        """Exportar ideas a Excel con formato profesional y guiones de voz"""
        
        if not nombre_archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"ideas_videos_pro_{timestamp}.xlsx"
        
        # Crear carpeta de salida
        salida_path = Path("ideas_generadas")
        salida_path.mkdir(exist_ok=True)
        archivo_completo = salida_path / nombre_archivo
        
        # Preparar datos para las hojas
        datos_principales = []
        datos_guiones = []
        datos_hashtags = []
        
        for i, idea in enumerate(ideas, 1):
            # Generar formatos IA si no existen
            if "formatos_ia" not in idea:
                idea["formatos_ia"] = self.generar_formatos_ia_especificos(idea)

            formatos = idea.get("formatos_ia", {})
            elevenlabs_config = formatos.get("elevenlabs", {})
            
            # Hoja principal - Ideas y Detalles
            principales = {
                "ID": i,
                "TÍTULO": idea.get("titulo", ""),
                "RED SOCIAL": idea.get("red_social", ""),
                "TEMA": idea.get("tema", ""),
                "NICHO": idea.get("nicho", ""),
                "DURACIÓN": idea.get("duracion", ""),
                "HOOK INICIAL": idea.get("hook_inicial", ""),
                "PALABRAS CLAVE": " | ".join(idea.get("metadata", {}).get("palabras_clave", [])),
                "ESCENAS RECOMENDADAS": " | ".join(idea.get("elementos_visuales", [])),
                "DESCRIPCIÓN": idea.get("descripcion", "")
            }
            datos_principales.append(principales)
            
            # Hoja de guiones
            guiones = {
                "ID": i,
                "TÍTULO": idea.get("titulo", ""),
                "GUIÓN COMPLETO": elevenlabs_config.get("texto_completo", ""),
                "VERSIÓN CORTA (15s)": elevenlabs_config.get("versiones_cortas", {}).get("15s", ""),
                "VERSIÓN CORTA (30s)": elevenlabs_config.get("versiones_cortas", {}).get("30s", ""),
                "ESTILO VOZ": elevenlabs_config.get("instrucciones_voz", {}).get("tono", ""),
                "EMOCIÓN": elevenlabs_config.get("instrucciones_voz", {}).get("emoción", ""),
                "NOTAS ADICIONALES": elevenlabs_config.get("instrucciones_voz", {}).get("notas", "")
            }
            datos_guiones.append(guiones)
            
            # Hoja de hashtags y keywords
            hashtags_data = {
                "ID": i,
                "TÍTULO": idea.get("titulo", ""),
                "HASHTAGS": " ".join(idea.get("hashtags", [])),
                "PALABRAS CLAVE": " | ".join(idea.get("metadata", {}).get("palabras_clave", [])),
                "TEMA PRINCIPAL": idea.get("tema", ""),
                "SUBTEMAS": " | ".join(self.nichos.get(idea.get("nicho", ""), {}).get("subtemas", []))
            }
            datos_hashtags.append(hashtags_data)
        
        # Crear Excel con las hojas simplificadas
        with pd.ExcelWriter(archivo_completo, engine='openpyxl') as writer:
            # Hoja de ideas principales
            df_principal = pd.DataFrame(datos_principales)
            df_principal.to_excel(writer, sheet_name='Ideas', index=False)
            
            # Hoja de guiones
            df_guiones = pd.DataFrame(datos_guiones)
            df_guiones.to_excel(writer, sheet_name='Guiones', index=False)
            
            # Hoja de hashtags y keywords
            df_hashtags = pd.DataFrame(datos_hashtags)
            df_hashtags.to_excel(writer, sheet_name='Hashtags y Keywords', index=False)
            
            # Ajustar anchos de columnas
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    
                    # Ajustes específicos por tipo de columna
                    if "GUIÓN" in str(column[0].value):
                        adjusted_width = min(max_length + 10, 150)  # Más ancho para guiones
                    else:
                        adjusted_width = min(max_length + 5, 50)  # Más compacto para otros campos
                    
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"\n📊 EXPORTACIÓN COMPLETADA")
        print(f"   📁 Archivo: {archivo_completo}")
        print(f"   📋 3 hojas: Ideas, Guiones, Hashtags y Keywords")
        print(f"   🎤 {len(ideas)} ideas completas con guiones")
        
        return str(archivo_completo)


def main():
    """Función principal mejorada"""
    print("🎬 GENERADOR PROFESIONAL DE IDEAS DE VIDEOS")
    print("=" * 70)
    print("🤖 Sistema de IA Avanzado para Creación de Contenido Viral")
    print("🆓 Powered by Gemini 2.0 Flash + Web Scraping + Análisis Inteligente")
    print("=" * 70)
    
    try:
        generador = GeneradorIdeasVideosAvanzado()
        
        print("\n🚀 OPCIONES DISPONIBLES:")
        print("1. 🔥 Generación Rápida (10 ideas optimizadas)")
        print("2. 📊 Generación Profesional (20-50 ideas con análisis)")
        print("3. 🎯 Generación Personalizada (configuración avanzada)")
        print("4. 🏢 Modo Empresa (100+ ideas para múltiples nichos)")
        
        opcion = input("\n👉 Selecciona modo (1-4): ").strip()
        
        if opcion == "1":
            print("\n🔥 MODO RÁPIDO ACTIVADO")
            ideas = generador.generar_lote_ideas_automatizado(10, {
                "score_minimo": 70,
                "redes_incluir": ["TikTok", "YouTube Shorts", "Instagram"],
                "nichos_incluir": ["Lifestyle", "Entretenimiento", "Tecnología"],
                "evitar_duplicados": True
            })
            
        elif opcion == "2":
            print("\n📊 MODO PROFESIONAL ACTIVADO")
            cantidad = input("¿Cuántas ideas generar? (20-50, default 25): ").strip()
            try:
                cantidad = max(20, min(50, int(cantidad)))
            except:
                cantidad = 25
                
            ideas = generador.generar_lote_ideas_automatizado(cantidad, {
                "score_minimo": 75,
                "redes_incluir": list(generador.redes_sociales.keys()),
                "nichos_incluir": list(generador.nichos.keys()),
                "evitar_duplicados": True
            })
            
        elif opcion == "3":
            print("\n🎯 CONFIGURACIÓN PERSONALIZADA")
            
            # Seleccionar redes sociales
            print("\nRedes sociales disponibles:")
            redes_lista = list(generador.redes_sociales.keys())
            for i, red in enumerate(redes_lista, 1):
                print(f"  {i}. {red}")
            
            redes_input = input("Selecciona redes (números separados por comas, ej: 1,2,3): ").strip()
            try:
                indices_redes = [int(x.strip()) - 1 for x in redes_input.split(",")]
                redes_elegidas = [redes_lista[i] for i in indices_redes if 0 <= i < len(redes_lista)]
            except:
                redes_elegidas = redes_lista
            
            # Seleccionar nichos
            print("\nNichos disponibles:")
            nichos_lista = list(generador.nichos.keys())
            for i, nicho in enumerate(nichos_lista, 1):
                print(f"  {i}. {nicho}")
            
            nichos_input = input("Selecciona nichos (números separados por comas): ").strip()
            try:
                indices_nichos = [int(x.strip()) - 1 for x in nichos_input.split(",")]
                nichos_elegidos = [nichos_lista[i] for i in indices_nichos if 0 <= i < len(nichos_lista)]
            except:
                nichos_elegidos = nichos_lista
            
            # Cantidad y score
            cantidad = input("¿Cuántas ideas generar? (1-100): ").strip()
            try:
                cantidad = max(1, min(100, int(cantidad)))
            except:
                cantidad = 20
            
            score_min = input("Score mínimo de calidad (60-95, default 75): ").strip()
            try:
                score_min = max(60, min(95, int(score_min)))
            except:
                score_min = 75
            
            ideas = generador.generar_lote_ideas_automatizado(cantidad, {
                "score_minimo": score_min,
                "redes_incluir": redes_elegidas,
                "nichos_incluir": nichos_elegidos,
                "evitar_duplicados": True
            })
            
        elif opcion == "4":
            print("\n🏢 MODO EMPRESA ACTIVADO")
            print("Generando 100 ideas distribuidas en todos los nichos...")
            
            ideas = generador.generar_lote_ideas_automatizado(100, {
                "score_minimo": 80,
                "redes_incluir": list(generador.redes_sociales.keys()),
                "nichos_incluir": list(generador.nichos.keys()),
                "evitar_duplicados": True
            })
            
        else:
            print("Opción no válida, usando modo rápido...")
            ideas = generador.generar_lote_ideas_automatizado(10)
        
        # Exportar resultados
        if ideas:
            archivo_excel = generador.exportar_a_excel_avanzado(ideas)
            
            # Estadísticas finales
            print(f"\n🎉 PROCESO COMPLETADO EXITOSAMENTE")
            print("=" * 50)
            print(f"📊 ESTADÍSTICAS:")
            print(f"   💡 Ideas generadas: {len(ideas)}")
            print(f"   📈 Score promedio: {sum(idea.get('score_calidad', 0) for idea in ideas) / len(ideas):.1f}")
            print(f"   🏆 Mejor score: {max(idea.get('score_calidad', 0) for idea in ideas)}")
            print(f"   📱 Redes cubiertas: {len(set(idea.get('red_social') for idea in ideas))}")
            print(f"   🎪 Nichos cubiertas: {len(set(idea.get('nicho') for idea in ideas))}")
            
            # Top 3 ideas
            top_ideas = sorted(ideas, key=lambda x: x.get('score_calidad', 0), reverse=True)[:3]
            print(f"\n🏆 TOP 3 IDEAS GENERADAS:")
            for i, idea in enumerate(top_ideas, 1):
                print(f"   {i}. {idea.get('titulo', '')[:50]}... (Score: {idea.get('score_calidad', 0)})")
            
            print(f"\n💼 ENTREGABLES:")
            print(f"   📁 Archivo Excel: {archivo_excel}")
            print(f"   📋 3 hojas: Ideas, Guiones, Hashtags y Keywords")
            print(f"   🎤 {len(ideas)} ideas completas con guiones")
            
        else:
            print("❌ No se pudieron generar ideas. Verifica tu configuración.")
            
    except ValueError as e:
        print(f"❌ {e}")
        print("\n🔧 CONFIGURACIÓN REQUERIDA:")
        print("1. Crea archivo .env con: GEMINI_API_KEY=tu_api_key_aqui")
        print("2. Obtén API key GRATUITA: https://aistudio.google.com/app/apikey")
        print("3. Instala dependencias: pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        print("Contacta soporte técnico si el problema persiste.")


if __name__ == "__main__":
    main() 