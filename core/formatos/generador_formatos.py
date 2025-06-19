"""
Módulo para generar formatos específicos para diferentes servicios de IA.
"""

from datetime import datetime

class GeneradorFormatos:
    """Clase para generar formatos específicos para diferentes servicios de IA."""
    
    def __init__(self):
        """Constructor de la clase GeneradorFormatos."""
        pass
    
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
            "tipo_contenido": "General",            "timestamp": datetime.now().isoformat()
        }
        
    def _generar_razon_impacto(self, punto):
        """Genera una razón de impacto para un punto dramático"""
        if not punto or len(punto) < 3:
            return "rompe con todas las expectativas del público"
            
        if "problema" in punto.lower() or "error" in punto.lower():
            return "la mayoría de personas comete este error sin darse cuenta y les cuesta miles de euros al año"
        elif "secreto" in punto.lower() or "truco" in punto.lower():
            return "las grandes empresas y expertos no quieren que esta información se difunda masivamente"
        elif "descubrimiento" in punto.lower() or "hallazgo" in punto.lower():
            return "contradice lo que se creía establecido hasta ahora en la industria"
        else:
            return "menos del 2% de las personas conoce esta información crucial"
            
    def _generar_consecuencia(self, punto):
        """Genera una consecuencia para un punto dramático"""
        if not punto or len(punto) < 3:
            return "cambia completamente nuestra perspectiva sobre el tema"
            
        if "beneficio" in punto.lower() or "ventaja" in punto.lower():
            return "puede multiplicar tus resultados en tiempo récord si lo aplicas correctamente"
        elif "estrategia" in punto.lower() or "técnica" in punto.lower():
            return "los que lo dominan tienen una ventaja competitiva inmensa sobre el resto"
        elif "evitar" in punto.lower() or "prevenir" in punto.lower():
            return "te ahorrará problemas graves que la mayoría enfrenta por ignorancia"
        else:
            return "te posiciona automáticamente en el top 5% de tu industria o nicho"
            
    def _generar_detalle_especifico(self, punto):
        """Genera un detalle específico para un punto narrativo"""
        if not punto or len(punto) < 3:
            return "revela una faceta completamente inesperada de la situación"
            
        palabras = punto.lower().split()
        if any(palabra in ["nunca", "jamás", "imposible"] for palabra in palabras):
            return "desafía todas las expectativas previas que teníamos sobre el tema"
        elif any(palabra in ["siempre", "todos", "cada"] for palabra in palabras):
            return "establece un patrón que se repite constantemente y que ahora podemos reconocer"
        else:
            return "introduce un elemento que reconfigura completamente nuestra comprensión"
            
    def _generar_leccion(self, descripcion, puntos_clave):
        """Genera una lección final basada en la historia"""
        if not puntos_clave:
            return "debemos estar atentos a los detalles inesperados que pueden cambiar todo"
            
        palabras_clave = []
        for punto in puntos_clave:
            palabras_clave.extend(punto.lower().split())
            
        if any(palabra in palabras_clave for palabra in ["aprender", "estudiar", "conocer", "saber"]):
            return "el conocimiento y la preparación siempre nos dan ventaja ante situaciones imprevistas"
        elif any(palabra in palabras_clave for palabra in ["éxito", "logro", "conseguir", "alcanzar"]):
            return "la perseverancia y actitud correcta son fundamentales para alcanzar resultados extraordinarios"
        elif any(palabra in palabras_clave for palabra in ["problema", "error", "fracaso", "dificultad"]):
            return "los obstáculos son oportunidades disfrazadas que nos permiten crecer y evolucionar"
        else:
            return "las decisiones pequeñas pueden tener un impacto enorme en nuestros resultados finales"
            
    def _generar_explicacion_practica(self, punto):
        """Genera una explicación práctica de un punto educativo"""
        if not punto or len(punto) < 3:
            return "establece la base fundamental para todo lo que viene después"
            
        palabras = punto.lower().split()
        if any(palabra in ["inicio", "comenzar", "empezar", "primer"] for palabra in palabras):
            return "te permite partir de una base sólida, evitando los errores comunes que comete el 90% de principiantes"
        elif any(palabra in ["optimizar", "mejorar", "aumentar", "incrementar"] for palabra in palabras):
            return "puede multiplicar tus resultados actuales entre un 30% y 70% sin necesidad de herramientas costosas"
        elif any(palabra in ["evitar", "prevenir", "reducir", "minimizar"] for palabra in palabras):
            return "te ahorra tiempo, dinero y frustración al identificar y corregir problemas desde el principio"
        else:
            return "establece un diferencial competitivo que menos del 5% de personas implementa correctamente"
            
    def _generar_ejemplo_practico(self, punto, nicho):
        """Genera un ejemplo práctico según el nicho"""
        ejemplos_por_nicho = {
            "Tecnología": "cuando implementé esta técnica en mi proyecto de desarrollo, el tiempo de carga se redujo un 47% en solo 3 días",
            "Marketing": "una campaña que estaba generando 1.2% de conversión pasó a 4.8% al implementar exactamente este enfoque",
            "Finanzas": "un portafolio de inversión estándar puede incrementar su rendimiento anual entre un 2% y 4% aplicando este principio",
            "Crecimiento Personal": "una persona con bloqueo creativo logró completar su proyecto en 2 semanas tras aplicar este método diariamente",
            "Inteligencia Artificial": "un modelo de IA mejoró su precisión del 78% al 93% simplemente ajustando este parámetro específico"
        }
        
        return ejemplos_por_nicho.get(nicho, "un cliente implementó este concepto y vio resultados tangibles en menos de una semana")
            
    def _generar_diferenciador(self, punto):
        """Genera un diferenciador para el último punto clave"""
        if not punto or len(punto) < 3:
            return "este es el factor que realmente marca la diferencia entre resultados mediocres y extraordinarios"
            
        palabras = punto.lower().split()
        if any(palabra in ["único", "especial", "diferente", "exclusivo"] for palabra in palabras):
            return "este enfoque personalizado genera resultados superiores al método estandarizado que todos conocen"
        elif any(palabra in ["rápido", "veloz", "inmediato", "instantáneo"] for palabra in palabras):
            return "puedes obtener resultados en días o semanas, no meses o años como enseñan tradicionalmente"
        elif any(palabra in ["fácil", "simple", "sencillo", "accesible"] for palabra in palabras):
            return "no necesitas herramientas complejas o conocimientos avanzados para implementarlo efectivamente"
        else:
            return "este enfoque sistemático garantiza resultados consistentes, no dependes de suerte o talento innato"
            
    def _generar_aplicacion_practica(self, punto, nicho):
        """Genera una aplicación práctica según el nicho"""
        aplicaciones_por_nicho = {
            "Tecnología": "implementa este principio en tu próximo proyecto técnico dedicándole 20 minutos diarios durante una semana",
            "Marketing": "aplica esta estrategia en tu próxima campaña publicitaria, midiendo los resultados antes y después",
            "Finanzas": "integra este criterio en tu próxima decisión financiera y documenta la diferencia en rendimiento",
            "Crecimiento Personal": "dedica 10 minutos cada mañana a esta práctica y registra los cambios en tu productividad después de 14 días",
            "Inteligencia Artificial": "ajusta este parámetro en tu modelo actual y compara los resultados con tu línea base"
        }
        
        return aplicaciones_por_nicho.get(nicho, "dedica 30 minutos esta semana a implementar este concepto y evalúa los resultados obtenidos")
            
    def _generar_beneficio(self, punto):
        """Genera un beneficio para un punto educativo"""
        if not punto or len(punto) < 3:
            return "impacta directamente en tus resultados finales y te diferencia de la competencia"
            
        palabras = punto.lower().split()
        if any(palabra in ["tiempo", "rápido", "veloz", "inmediato"] for palabra in palabras):
            return "te permite optimizar tu tiempo, logrando más resultados con menos esfuerzo"
        elif any(palabra in ["dinero", "costo", "inversión", "precio"] for palabra in palabras):
            return "mejora significativamente el retorno sobre tu inversión, maximizando cada recurso"
        elif any(palabra in ["calidad", "valor", "premium", "excelencia"] for palabra in palabras):
            return "eleva el nivel de calidad de tu trabajo a estándares profesionales de primer nivel"
        else:
            return "te proporciona una ventaja competitiva sostenible a largo plazo"
            
    def _generar_recomendacion_especifica(self, punto, nicho):
        """Genera una recomendación específica según el nicho"""
        recomendaciones_por_nicho = {
            "Tecnología": "utilices herramientas de diagnóstico específicas para identificar oportunidades de optimización",
            "Marketing": "segmentes tu audiencia aplicando estos criterios antes de lanzar cualquier campaña",
            "Finanzas": "evalúes cada inversión utilizando estos 3 indicadores clave antes de comprometer capital",
            "Crecimiento Personal": "establezcas un sistema de seguimiento diario para monitorear tu progreso",
            "Inteligencia Artificial": "validez tus modelos con este enfoque para mejorar significativamente la precisión"
        }
        
        return recomendaciones_por_nicho.get(nicho, "implementes este concepto gradualmente, midiendo los resultados en cada fase")
            
    def _generar_paso_accion(self, puntos_clave, indice):
        """Genera un paso de acción basado en los puntos clave"""
        if not puntos_clave or indice >= len(puntos_clave):
            pasos_genericos = [
                "Identifica las áreas específicas donde puedes aplicar estos principios",
                "Implementa gradualmente estos conceptos, midiendo resultados en cada fase",
                "Evalúa y ajusta tu estrategia basándote en los datos obtenidos"
            ]
            return pasos_genericos[indice % len(pasos_genericos)]
            
        punto = puntos_clave[indice]
        if indice == 0:
            return f"Comienza por {punto.lower().split()[0]} {' '.join(punto.lower().split()[1:])} durante al menos 7 días consecutivos"
        elif indice == len(puntos_clave) - 1:
            return f"Integra {punto.lower()} como parte de tu rutina habitual para maximizar resultados"
        else:
            return f"Después de dominar lo básico, profundiza en {punto.lower()} con práctica consistente"
            
    def _generar_beneficio_final(self, descripcion, nicho):
        """Genera un beneficio final personalizado por nicho"""
        beneficios_por_nicho = {
            "Tecnología": "optimizarás significativamente tus sistemas y procesos, logrando mayor eficiencia con menos recursos",
            "Marketing": "incrementarás tus conversiones y engagement de manera medible y sostenible",
            "Finanzas": "maximizarás tu retorno de inversión mientras minimizas riesgos innecesarios",
            "Crecimiento Personal": "experimentarás mejoras tangibles en tu productividad y satisfacción personal",
            "Inteligencia Artificial": "desarrollarás modelos más precisos y eficientes que resolverán problemas reales"
        }
        
        return beneficios_por_nicho.get(nicho, "obtendrás resultados superiores de manera consistente y predecible")

    def generar_formatos_ia_especificos(self, idea):
        """Generar formatos específicos para diferentes servicios de IA"""
        
        titulo = idea.get("titulo", "")
        descripcion = idea.get("descripcion", "")
        puntos_clave = idea.get("puntos_clave", [])
        tipo_contenido = idea.get("tipo_contenido", "educativo")
        nicho = idea.get("nicho", "")
        tema = idea.get("tema", "")
        
        # Configurar estilo de voz según el tipo de contenido
        if tipo_contenido == "narrativo" or nicho == "Historias Reddit":
            estilo_voz = {
                "tono": "narrativo y dinámico",
                "velocidad": "variable según la tensión",
                "emoción": "expresivo y dramático"
            }
            # Generar guión narrativo y dramático con detalles específicos
            guion_voz = f"""¡No van a creer esta historia real sobre {titulo}!

El hook inicial: {idea.get('hook_inicial', 'Una situación inesperada que cambió todo')}

{descripcion}

"""
            # Añadir puntos clave como elementos dramáticos con detalles concretos
            for i, punto in enumerate(puntos_clave, 1):
                if i == 1:
                    guion_voz += f"""Primero, lo más impactante: {punto}
Esto NO es algo que suele verse todos los días, y la razón es que {self._generar_razon_impacto(punto)}.

"""
                elif i == len(puntos_clave):
                    guion_voz += f"""Y finalmente, el detalle que NADIE esperaba: {punto}
Lo que hace esto tan sorprendente es que {self._generar_consecuencia(punto)}.

"""
                else:
                    guion_voz += f"""Después ocurrió algo más: {punto}
Esto cambió completamente la situación porque {self._generar_detalle_especifico(punto)}.

"""
            
            # Cierre dramático con llamada a la acción específica
            guion_voz += f"""
La conclusión de esta historia nos enseña que {self._generar_leccion(descripcion, puntos_clave)}.

¿Han vivido algo similar? Cuéntenme su experiencia en los comentarios.
Si quieren más historias sobre {tema}, den like y activen la campanita.
"""

        else:
            estilo_voz = {
                "tono": "profesional y educativo",
                "velocidad": "clara y pausada",
                "emoción": "entusiasta y confiado"
            }
            # Generar guión educativo y profesional con información concreta y útil
            guion_voz = f"""¡Hola! Hoy te traigo {titulo} - información que realmente necesitas saber.

{idea.get('hook_inicial', '¿Sabías que la mayoría de personas comete errores en este tema?')}

{descripcion}

En este video te voy a dar información específica y aplicable, no solo teoría.

"""
            # Añadir puntos clave como lecciones con ejemplos prácticos
            for i, punto in enumerate(puntos_clave, 1):
                if i == 1:
                    guion_voz += f"""El primer punto clave es: {punto}
Esto es fundamental porque {self._generar_explicacion_practica(punto)}.
Un ejemplo concreto: {self._generar_ejemplo_practico(punto, nicho)}.

"""
                elif i == len(puntos_clave):
                    guion_voz += f"""Finalmente, y esto es lo que marca la diferencia: {punto}
A diferencia de lo que muchos creen, {self._generar_diferenciador(punto)}.
Aplícalo así: {self._generar_aplicacion_practica(punto, nicho)}.

"""
                else:
                    guion_voz += f"""El siguiente aspecto importante: {punto}
Este punto es esencial porque {self._generar_beneficio(punto)}.
Te recomiendo que {self._generar_recomendacion_especifica(punto, nicho)}.

"""
            
            # Cierre educativo con resumen de valor y aplicaciones reales
            guion_voz += f"""
Para implementar lo que hemos aprendido hoy sobre {titulo}:
1. {self._generar_paso_accion(puntos_clave, 0)}
2. {self._generar_paso_accion(puntos_clave, 1)}
3. {self._generar_paso_accion(puntos_clave, 2)}

El beneficio real de aplicar estos conocimientos es que {self._generar_beneficio_final(descripcion, nicho)}.

Si este contenido te resultó útil, apóyalo con un like y suscríbete para más contenido práctico como este.
¿Qué aspecto de {tema} te gustaría que profundice en un próximo video?
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
        # Implementación simple para mantener compatibilidad
        return []

    def generar_prompt_runway(self, idea):
        """Generar prompt para Runway ML"""
        # Implementación simple para mantener compatibilidad
        return ""

    def generar_guia_capcut(self, idea):
        """Generar guía para CapCut"""
        # Implementación simple para mantener compatibilidad
        return ""

    def generar_prompt_midjourney(self, idea):
        """Generar prompt para Midjourney"""
        # Implementación simple para mantener compatibilidad
        return ""
