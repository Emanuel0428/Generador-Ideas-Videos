"""
Paquete core para el Generador de Ideas de Videos.
Este paquete contiene todos los módulos principales del generador.
"""

# Importaciones principales para facilitar el acceso a las clases principales
from core.config.configuracion_contenido import ConfiguracionContenido
from core.tendencias.recopilador_tendencias import RecopiladorTendencias
from core.generador.generador_ideas import GeneradorIdeas
from core.formatos.generador_formatos import GeneradorFormatos
from core.exportador.exportador import ExportadorIdeas

# Definir qué clases se importan con 'from core import *'
__all__ = [
    'ConfiguracionContenido',
    'RecopiladorTendencias',
    'GeneradorIdeas',
    'GeneradorFormatos',
    'ExportadorIdeas'
]