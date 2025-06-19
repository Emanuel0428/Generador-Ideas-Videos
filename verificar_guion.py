#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar el contenido de los guiones generados.
"""

import pandas as pd
import glob
import os
from pathlib import Path

def mostrar_ultimo_guion():
    """Muestra el contenido del guión del último archivo Excel generado."""
    # Encontrar el archivo Excel más reciente
    directorio = Path("ideas_generadas")
    archivos = list(directorio.glob("*.xlsx"))
    archivos.sort(key=os.path.getmtime, reverse=True)
    
    if not archivos:
        print("❌ No se encontraron archivos Excel generados.")
        return
    
    ultimo_archivo = archivos[0]
    print(f"\n📊 Analizando archivo: {ultimo_archivo.name}\n")
    
    # Leer el archivo Excel
    try:
        # Intentar cargar la hoja de ideas
        try:
            df_ideas = pd.read_excel(ultimo_archivo, sheet_name="Ideas")
            print(f"✅ Hoja 'Ideas' encontrada: {len(df_ideas)} ideas")
        except:
            print("❌ No se pudo cargar la hoja 'Ideas'")
            
        # Cargar la hoja de guiones
        df_guiones = pd.read_excel(ultimo_archivo, sheet_name="Guiones")
        print(f"✅ Hoja 'Guiones' encontrada: {len(df_guiones)} guiones\n")
        
        # Mostrar los primeros 3 guiones
        for i, fila in df_guiones.head(3).iterrows():
            print(f"\n{'=' * 80}")
            print(f"📝 GUIÓN #{i+1}: {fila.get('Título', 'Sin título')}")
            print(f"🎯 Nicho: {fila.get('Nicho', 'Sin nicho')} | 📱 Red: {fila.get('Red Social', 'Sin red')}")
            print(f"{'=' * 80}")
            
            # Encontrar la columna que tiene el guión (puede variar el nombre)
            guion_col = None
            for col in df_guiones.columns:
                if 'guion' in col.lower() or 'guión' in col.lower():
                    guion_col = col
                    break
                    
            if guion_col:
                contenido = fila[guion_col]
                if isinstance(contenido, str):
                    print(contenido[:500] + "..." if len(contenido) > 500 else contenido)
                else:
                    print("❌ El contenido no es texto")
            else:
                print("❌ No se encontró la columna del guión")
                
            print("\n" + "-" * 40)
    
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")

if __name__ == "__main__":
    mostrar_ultimo_guion()
