"""
Módulo de configuración para el Generador de Ideas de Videos.
Gestiona la carga de API keys y configuraciones comunes.
"""

import os
from pathlib import Path

def cargar_api_key():
    """Cargar API key de Gemini desde variables de entorno o archivo .env"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key and os.path.exists(".env"):
        try:
            with open(".env") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY"):
                        api_key = line.strip().split("=", 1)[1].strip().strip('"\'')
        except:
            pass
    
    if not api_key:
        raise ValueError("❌ No se encontró GEMINI_API_KEY. Ponla en .env o como variable de entorno.")
    
    return api_key

def obtener_ruta_salida():
    """Obtiene y crea si es necesario la carpeta de salida para las ideas generadas"""
    salida_path = Path("ideas_generadas")
    salida_path.mkdir(exist_ok=True)
    return salida_path
