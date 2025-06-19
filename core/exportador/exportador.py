"""
Módulo para exportar ideas a diferentes formatos.
"""

import pandas as pd
from datetime import datetime
from pathlib import Path

class ExportadorIdeas:
    """Clase para exportar ideas a diferentes formatos."""
    
    def __init__(self, salida_path=None):
        """Constructor de la clase ExportadorIdeas.
        
        Args:
            salida_path: Ruta donde guardar los archivos exportados.
        """
        # Crear carpeta de salida si no se proporciona
        self.salida_path = salida_path or Path("ideas_generadas")
        self.salida_path.mkdir(exist_ok=True)
    
    def exportar_a_excel_avanzado(self, ideas, nombre_archivo=None):
        """Exportar ideas a Excel con formato profesional y guiones de voz"""
        
        if not nombre_archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"ideas_videos_pro_{timestamp}.xlsx"
        
        archivo_completo = self.salida_path / nombre_archivo
        
        # Preparar datos para las hojas
        datos_principales = []
        datos_guiones = []
        datos_hashtags = []
        
        for i, idea in enumerate(ideas, 1):
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
            
            # Extraer configuración de guiones
            formatos = idea.get("formatos_ia", {})
            elevenlabs_config = formatos.get("elevenlabs", {})
            
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
                "SUBTEMAS": " | ".join(idea.get("metadata", {}).get("subtemas", []))
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
