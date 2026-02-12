import os
import sys
import shutil
from markdownify import markdownify as md

def procesar_directorio(ruta_origen):
    # Definir ruta de origen absoluta y carpeta de salida
    origen_abs = os.path.abspath(ruta_origen)
    base_salida = os.path.abspath("SALIDA")

    # Verificar que el origen existe
    if not os.path.exists(origen_abs):
        print(f"❌ Error: La ruta '{ruta_origen}' no existe.")
        return

    print(f"📂 Origen: {origen_abs}")
    print(f"📂 Destino: {base_salida}")
    print("--- Comenzando proceso ---")

    # Recorrer el directorio recursivamente
    for raiz, directorios, archivos in os.walk(origen_abs):
        # Calcular la ruta relativa para replicar la estructura
        ruta_relativa = os.path.relpath(raiz, origen_abs)
        
        # Determinar directorio destino actual
        if ruta_relativa == ".":
            dir_destino = base_salida
        else:
            dir_destino = os.path.join(base_salida, ruta_relativa)

        # Crear el directorio si no existe
        if not os.path.exists(dir_destino):
            os.makedirs(dir_destino)

        for archivo in archivos:
            ruta_archivo_origen = os.path.join(raiz, archivo)
            nombre, extension = os.path.splitext(archivo)
            
            # Si es HTML, convertir a Markdown
            if extension.lower() in ['.html', '.htm']:
                ruta_archivo_final = os.path.join(dir_destino, nombre + ".md")
                try:
                    with open(ruta_archivo_origen, 'r', encoding='utf-8', errors='ignore') as f:
                        contenido_html = f.read()
                    
                    # Convertir HTML a Markdown
                    contenido_md = md(contenido_html, heading_style="ATX")
                    
                    with open(ruta_archivo_final, 'w', encoding='utf-8') as f:
                        f.write(contenido_md)
                    print(f"✅ Convertido: {archivo} -> {nombre}.md")
                except Exception as e:
                    print(f"⚠️ Error convirtiendo {archivo}: {e}")

            # Si NO es HTML, copiar tal cual
            else:
                ruta_archivo_final = os.path.join(dir_destino, archivo)
                try:
                    shutil.copy2(ruta_archivo_origen, ruta_archivo_final)
                    print(f"📋 Copiado: {archivo}")
                except Exception as e:
                    print(f"⚠️ Error copiando {archivo}: {e}")

    print("\n🎉 Proceso finalizado. Revisa la carpeta 'SALIDA'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 convertidor.py <ruta_del_directorio>")
    else:
        procesar_directorio(sys.argv[1])
