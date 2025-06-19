"""
Módulo principal para la generación de ideas con IA.
"""

import google.generativeai as genai
import random
import re
from datetime import datetime

class GeneradorIdeas:
    """Clase para generar ideas de videos usando IA."""
    
    def __init__(self, api_key, configuracion_contenido):
        """Inicializa el generador de ideas.
        
        Args:
            api_key: API key de Gemini
            configuracion_contenido: Objeto ConfiguracionContenido con la configuración de redes y nichos
        """
        self.api_key = api_key
        self.configuracion_contenido = configuracion_contenido
        self.configurar_gemini()
        self.ideas_generadas_sesion = []
    
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
    
    def generar_idea_con_ia(self, tema, red_social, nicho=None, tipo_contenido=None):
        """Genera una idea de contenido usando IA, con enfoque educativo o narrativo según el nicho"""
        try:
            # Configurar el prompt según el nicho y su enfoque
            nichos = self.configuracion_contenido.nichos
            
            if nicho in nichos:
                nicho_info = nichos[nicho]
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
                    Hook: [hook inicial impactante de 1-2 frases]
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
                    Hook: [hook inicial impactante de 1-2 frases]
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
            if nicho in nichos:
                idea_json["enfoque"] = "educativo" if nichos[nicho].get("enfoque_educativo", True) else "narrativo"
                idea_json["estilo"] = nichos[nicho].get("estilo", "general")
                idea_json["audiencia_objetivo"] = nichos[nicho].get("audiencia", "general")

            return idea_json

        except Exception as e:
            print(f"❌ Error generando idea: {str(e)}")
            return None
            
    def procesar_respuesta_ia(self, texto_respuesta, tema, red_social, nicho=None):
        """Procesa y estructura la respuesta de la IA según el nicho"""
        try:
            nichos = self.configuracion_contenido.nichos
            
            # Estructura base para la idea
            idea_estructurada = {
                "tema": tema,
                "red_social": red_social,
                "nicho": nicho,
                "titulo": "",
                "descripcion": "",
                "puntos_clave": [],
                "hashtags": [],
                "hook_inicial": "",
                "tipo_contenido": "educativo" if nicho and nichos[nicho].get("enfoque_educativo", True) else "narrativo",
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
                elif "hook:" in linea.lower():
                    idea_estructurada["hook_inicial"] = linea.split(":", 1)[1].strip()
                elif "descripción:" in linea.lower() or "descripcion:" in linea.lower():
                    seccion_actual = "descripcion"
                    idea_estructurada["descripcion"] = linea.split(":", 1)[1].strip()
                elif "puntos clave:" in linea.lower():
                    seccion_actual = "puntos_clave"
                elif "- " in linea and (seccion_actual == "puntos_clave" or not seccion_actual):
                    idea_estructurada["puntos_clave"].append(linea[2:].strip())
                elif "hashtags:" in linea.lower() or "#" in linea:
                    hashtags = re.findall(r'#\w+', linea)
                    idea_estructurada["hashtags"].extend(hashtags)

            # Generar puntos clave si no se encontraron
            if not idea_estructurada["puntos_clave"]:
                idea_estructurada["puntos_clave"] = self._generar_puntos_clave_por_defecto(tema, nicho, idea_estructurada["titulo"], idea_estructurada["descripcion"])
                
            # Generar hook inicial si no se encontró
            if not idea_estructurada["hook_inicial"]:
                idea_estructurada["hook_inicial"] = self._generar_hook_inicial(idea_estructurada["titulo"], tema, nicho)

            # Añadir metadatos específicos según el nicho
            if nicho in nichos:
                idea_estructurada["metadata"].update({
                    "estilo": nichos[nicho].get("estilo", "general"),
                    "audiencia": nichos[nicho].get("audiencia", "general"),
                    "palabras_clave": nichos[nicho].get("palabras_clave", [])
                })

            return idea_estructurada
                
        except Exception as e:
            print(f"❌ Error procesando respuesta: {str(e)}")
            return None
    
    def _generar_puntos_clave_por_defecto(self, tema, nicho, titulo, descripcion):
        """Genera puntos clave por defecto basados en el tema y nicho"""
        puntos_clave = []
        
        if not nicho:
            return ["Estrategias efectivas", "Mejores prácticas", "Consejos de implementación"]
            
        if nicho == "Marketing":
            puntos_clave = [
                f"La estrategia de {tema} más efectiva en 2024 según datos reales",
                f"3 errores comunes que arruinan tus resultados con {tema}",
                f"Cómo implementar {tema} para duplicar conversiones en 30 días"
            ]
        elif nicho == "Tecnología":
            puntos_clave = [
                f"Impacto de {tema} en el desarrollo tecnológico actual",
                f"Comparativa de las mejores herramientas para {tema}",
                f"Tutorial paso a paso: Implementando {tema} en tu proyecto"
            ]
        elif nicho == "Crecimiento Personal":
            puntos_clave = [
                f"El método comprobado para dominar {tema} en 21 días",
                f"Cómo {tema} impacta tu productividad y resultados diarios",
                f"Sistema de seguimiento para medir tu progreso en {tema}"
            ]
        elif nicho == "Finanzas":
            puntos_clave = [
                f"El impacto de {tema} en tu estabilidad financiera",
                f"Estrategia de inversión basada en {tema} para resultados consistentes",
                f"Análisis de riesgo y retorno aplicando {tema}"
            ]
        elif nicho == "Inteligencia Artificial":
            puntos_clave = [
                f"Cómo {tema} está transformando la industria de IA",
                f"Implementación práctica de {tema} en proyectos de machine learning",
                f"Casos de estudio: Empresas que han revolucionado con {tema}"
            ]
        else:
            # Puntos genéricos pero específicos
            palabras = titulo.split() + descripcion.split() + tema.split()
            palabras_clave = [palabra for palabra in palabras if len(palabra) > 4]
            
            if palabras_clave:
                palabra = random.choice(palabras_clave)
                puntos_clave = [
                    f"La verdad sobre {palabra} que nadie te cuenta",
                    f"3 técnicas avanzadas para dominar {tema}",
                    f"Resultados reales: Antes y después de implementar {tema}"
                ]
            else:
                puntos_clave = [
                    f"Estrategia práctica para implementar {tema}",
                    f"Los 3 principales beneficios de dominar {tema}",
                    f"Cómo medir y optimizar tus resultados con {tema}"
                ]
                
        return puntos_clave
        
    def _generar_hook_inicial(self, titulo, tema, nicho):
        """Genera un hook inicial impactante basado en el título y nicho"""
        # Si no hay nicho, usar hook genérico pero efectivo
        if not nicho:
            return f"¿Sabías que el 83% de personas fracasa con {tema} por este simple error?"
            
        # Hooks específicos por nicho para mayor relevancia
        hooks_por_nicho = {
            "Marketing": [
                f"¿Cansado de estrategias de {tema} que NO dan resultados? Esto cambiará todo.",
                f"La mayoría de marketers arruina su {tema} por este error que nadie menciona.",
                f"Descubrí una estrategia de {tema} que duplicó mis conversiones en solo 14 días."
            ],
            "Tecnología": [
                f"Este avance en {tema} está haciendo obsoletas las técnicas tradicionales.",
                f"El 91% de desarrolladores implementa {tema} incorrectamente. ¿Eres uno de ellos?",
                f"La forma en que usas {tema} puede estar comprometiendo todo tu sistema."
            ],
            "Crecimiento Personal": [
                f"Descubrí por qué el 97% nunca alcanza su potencial con {tema}.",
                f"Esta técnica de {tema} transformó mi productividad en solo 7 días.",
                f"El método que cambió mi relación con {tema} para siempre."
            ],
            "Finanzas": [
                f"Este error con {tema} está drenando tu dinero sin que lo notes.",
                f"Cómo aumenté mis ganancias un 32% implementando correctamente {tema}.",
                f"La estrategia de {tema} que los expertos financieros usan en secreto."
            ],
            "Inteligencia Artificial": [
                f"Esta implementación de {tema} está revolucionando la industria tech en 2024.",
                f"El 88% de modelos de IA fallan por no optimizar correctamente {tema}.",
                f"La nueva era de {tema} que está dejando obsoletos los métodos anteriores."
            ]
        }
        
        # Seleccionar hook específico o usar uno genérico
        if nicho in hooks_por_nicho:
            return random.choice(hooks_por_nicho[nicho])
        else:
            return f"¿Sabías que el 78% de personas nunca aprovecha todo el potencial de {tema}? Esto cambiará tu perspectiva."
    
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
    
    def generar_lote_ideas_automatizado(self, cantidad=20, filtros=None, tendencias=None):
        """Generar lote de ideas de forma completamente automatizada
        
        Args:
            cantidad: Número de ideas a generar
            filtros: Diccionario con filtros a aplicar
            tendencias: Lista de tendencias a utilizar
        """
        
        print(f"🤖 GENERACIÓN AUTOMATIZADA DE {cantidad} IDEAS PROFESIONALES")
        print("=" * 70)
        
        # Obtener tendencias si no se proporcionan
        if not tendencias:
            raise ValueError("Se deben proporcionar tendencias para generar ideas")
        
        ideas_generadas = []
        ideas_exitosas = 0
        intentos = 0
        max_intentos = cantidad * 2
        
        # Filtros por defecto
        if not filtros:
            filtros = {
                "score_minimo": 50,
                "redes_incluir": list(self.configuracion_contenido.redes_sociales.keys()),
                "nichos_incluir": ["Tecnología", "Crecimiento Personal", "Marketing", "Finanzas", "Inteligencia Artificial", "Historias Reddit"],
                "evitar_duplicados": True
            }
            
        # Validar que los nichos existan
        nichos_validos = [nicho for nicho in filtros["nichos_incluir"] if nicho in self.configuracion_contenido.nichos]
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
        nichos = self.configuracion_contenido.nichos
        
        if nicho not in nichos:
            return tema
            
        palabras_clave = nichos[nicho]["palabras_clave"]
        subtemas = nichos[nicho]["subtemas"]
        
        # Seleccionar aleatoriamente un enfoque
        if random.random() < 0.5:
            # Usar palabra clave
            palabra_clave = random.choice(palabras_clave)
            return f"{palabra_clave} {tema}"
        else:
            # Usar subtema
            subtema = random.choice(subtemas)
            return f"{tema} en {subtema}"
