"""
Módulo que define las configuraciones de redes sociales y nichos.
"""

class ConfiguracionContenido:
    """Clase para gestionar las configuraciones de redes sociales y nichos."""
    
    def __init__(self):
        """Constructor de la clase ConfiguracionContenido."""
        self.redes_sociales = self.configurar_redes_sociales()
        self.nichos = self.configurar_nichos()
        self.templates = self.configurar_templates()
    
    def obtener_redes_sociales(self):
        """Devuelve la configuración de redes sociales."""
        return self.redes_sociales
        
    def obtener_nichos(self):
        """Devuelve la configuración de nichos."""
        return self.nichos
        
    def obtener_templates(self):
        """Devuelve la configuración de templates."""
        return self.templates
        
    def configurar_redes_sociales(self):
        """Configuración avanzada de redes sociales con métricas y algoritmos"""
        return {
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
        return {
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
        templates = {
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
        templates.update({
            "viral_hook": templates.get("viral_hook", []),
            "educational": templates.get("educational", []),
            "comparison": templates.get("comparison", []),
            "trending": templates.get("trending", [])
        })
        
        return templates
