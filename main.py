#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generador Profesional de Ideas de Videos
Sistema Avanzado de Generación Automatizada de Ideas de Videos
"""

from core.config.config import cargar_api_key, obtener_ruta_salida
from core.config.configuracion_contenido import ConfiguracionContenido
from core.tendencias.recopilador_tendencias import RecopiladorTendencias
from core.generador.generador_ideas import GeneradorIdeas
from core.formatos.generador_formatos import GeneradorFormatos
from core.exportador.exportador import ExportadorIdeas


class GeneradorIdeasVideosAvanzado:
    """Clase principal que integra todos los módulos del generador de ideas."""
    
    def __init__(self):
        """Inicializa el generador de ideas de videos."""
        print("🚀 Inicializando Generador de Ideas Profesional...")
        
        # Cargar configuración y dependencias
        self.api_key = cargar_api_key()
        self.configuracion = ConfiguracionContenido()
        self.recopilador = RecopiladorTendencias()
        self.generador = GeneradorIdeas(self.api_key, self.configuracion)
        self.formateador = GeneradorFormatos()
        self.exportador = ExportadorIdeas(obtener_ruta_salida())
        
        # Acceso rápido a configuraciones
        self.redes_sociales = self.configuracion.obtener_redes_sociales()
        self.nichos = self.configuracion.obtener_nichos()
          
    def generar_lote_ideas_automatizado(self, cantidad=20, filtros=None):
        """Genera un lote de ideas automatizado.
        
        Args:
            cantidad: Número de ideas a generar
            filtros: Diccionario con filtros para las ideas
            
        Returns:
            Lista de ideas generadas
        """
        # Obtener tendencias actuales
        tendencias = self.recopilador.obtener_todas_las_tendencias()
        
        # Generar ideas con las tendencias obtenidas
        ideas = self.generador.generar_lote_ideas_automatizado(cantidad, filtros, tendencias)
        
        # Generar formatos específicos para cada idea
        for idea in ideas:
            idea["formatos_ia"] = self.formateador.generar_formatos_ia_especificos(idea)
        
        return ideas
    
    def exportar_ideas(self, ideas, nombre_archivo=None):
        """Exporta las ideas generadas a un archivo Excel.
        
        Args:
            ideas: Lista de ideas a exportar
            nombre_archivo: Nombre del archivo de salida
            
        Returns:
            Ruta del archivo Excel generado
        """
        return self.exportador.exportar_a_excel_avanzado(ideas, nombre_archivo)


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
            archivo_excel = generador.exportar_ideas(ideas)
            
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
