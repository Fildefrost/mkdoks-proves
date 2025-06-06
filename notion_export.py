import os
import shutil
import sys
import re
import urllib.parse
from pathlib import Path
from collections import defaultdict

# Rutas base del proyecto
ROOT = Path(__file__).resolve().parent
EXPORT_DIR = ROOT / "notion_export"
WRITEUPS_DIR = ROOT / "Writeup-ctfs"
NAV_FILE = ROOT / "nav_generated.yml"

# Regex para detectar el hash que añade Notion al nombre de archivo/carpeta
HASH_PATTERN = re.compile(r"\s[0-9a-f]{32}$", re.IGNORECASE)

def limpiar_hash(nombre: str) -> str:
    """
    Elimina el hash de Notion de los nombres de los archivos o carpetas.
    Ejemplo: "BocataCalamares 19b3abc..." -> "BocataCalamares"
    """
    return HASH_PATTERN.sub("", nombre).strip()

def embellecer_cabecera(md_text: str, titulo: str) -> str:
    """
    Mejora el bloque de metadatos de los writeups en Markdown.
    Inserta título (#), iconos, y separador visual.
    """
    pattern = re.compile(
        r"Plataforma: (?P<plataforma>.+?)\s+OS: (?P<os>.+?)\s+Level: (?P<level>.+?)\s+Status: (?P<status>.+?)\s+Complete: (?P<complete>.+?)\s+EJPT: (?P<ejpt>.+?)\s+Created time: (?P<created>.+?)\s+IP: (?P<ip>[^\n]+)"
    )

    match = pattern.search(md_text)
    if not match:
        # Si no hay metadatos, insertar solo título y separador
        return f"# {titulo}\n\n---\n\n" + md_text

    # Genera una cabecera Markdown rica visualmente
    cabecera_md = (
        f"# {titulo}\n\n"
        f"> 🧠 **Plataforma:** {match['plataforma']}\n>\n"
        f"> 💻 **Sistema operativo:** {match['os']}\n>\n"
        f"> 🎯 **Nivel:** {match['level']}\n>\n"
        f"> ✅ **Estado:** {match['status']}\n>\n"
        f"> 📘 **Curso eJPT:** {match['ejpt']}\n>\n"
        f"> 🗓️ **Fecha de creación:** {match['created']}\n>\n"
        f"> 🌐 **IP:** `{match['ip']}`\n\n"
        f"---\n"
    )

    return md_text.replace(match.group(0), cabecera_md, 1)

def procesar_writeup(md_path: Path, plataforma: str, resumen: list, nav_dict: dict):
    """
    Procesa un archivo .md exportado desde Notion:
    - Limpia su nombre
    - Mueve y renombra imágenes
    - Reemplaza rutas en el .md
    - Aplica cabecera visual
    """
    nombre_md_original = md_path.stem
    base_name = limpiar_hash(nombre_md_original)

    plataforma_dir = WRITEUPS_DIR / plataforma
    imagenes_dir = plataforma_dir / "imagenes"
    imagenes_origen = md_path.parent / nombre_md_original  # Carpeta de imágenes exportada por Notion

    md_dest = plataforma_dir / f"{base_name}.md"

    if md_dest.exists():
        resumen.append((base_name, "❌ Ya existe, omitido"))
        return

    # Leer el contenido del .md original
    content = md_path.read_text(encoding="utf-8")

    imagen_renombrada = {}

    # Mover y renombrar imágenes
    if imagenes_origen.exists() and imagenes_origen.is_dir():
        for imagen in imagenes_origen.iterdir():
            nuevo_nombre = f"{base_name}_{imagen.name}"  # Preserva espacios en nombres
            imagen_dest = imagenes_dir / nuevo_nombre
            imagenes_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(imagen), imagen_dest)
            imagen_renombrada[imagen.name] = nuevo_nombre

    # Reemplazo de rutas de imagen en el contenido
    def replace_img_path(match):
        alt_text = match.group(1)
        encoded_path = os.path.basename(match.group(2))
        original_path = urllib.parse.unquote(encoded_path)  # Convierte %20 → espacio

        nuevo_path = imagen_renombrada.get(original_path)
        if nuevo_path:
            return f"![{alt_text}](./imagenes/{nuevo_path})"
        else:
            print(f"⚠️ Imagen no encontrada o no renombrada: {original_path}")
            return f"![{alt_text}]({match.group(2)}) <!-- IMAGEN NO RENOMBRADA: {original_path} -->"

    content = re.sub(r"!\[(.*?)\]\((.*?)\)", replace_img_path, content)

    # Embellecer cabecera con título y metadatos
    content = embellecer_cabecera(content, base_name)

    # Crear carpeta si no existe y guardar el archivo .md
    md_dest.parent.mkdir(parents=True, exist_ok=True)
    md_dest.write_text(content, encoding="utf-8")

    # Eliminar carpeta de imágenes original exportada por Notion
    if imagenes_origen.exists():
        shutil.rmtree(imagenes_origen)

    # Eliminar el .md original de notion_export
    md_path.unlink()

    resumen.append((base_name, "✅ Importado correctamente"))
    nav_dict[plataforma].append((base_name, f"Writeup-ctfs/{plataforma}/{base_name}.md"))

def guardar_nav(nav_dict: dict):
    """
    Genera el archivo nav_generated.yml con la estructura de navegación
    para MkDocs (usado con !include)
    """
    with open(NAV_FILE, "w", encoding="utf-8") as f:
        f.write("nav:\n")
        for plataforma in sorted(nav_dict):
            f.write(f"  - {plataforma}:\n")
            for nombre, ruta in sorted(nav_dict[plataforma]):
                f.write(f"      - {nombre}: {ruta}\n")
    print(f"\n✅ Archivo actualizado: nav_generated.yml\n")

def main():
    """
    Punto de entrada del script. Espera una plataforma como argumento.
    """
    if len(sys.argv) < 2:
        print("❌ Uso: python notion_export.py <Plataforma>")
        sys.exit(1)

    plataforma = sys.argv[1]
    if not EXPORT_DIR.exists():
        print("❌ La carpeta 'notion_export/' no existe.")
        sys.exit(1)

    resumen = []
    nav_dict = defaultdict(list)

    # Procesar todos los archivos .md dentro de notion_export/
    for md_file in EXPORT_DIR.rglob("*.md"):
        procesar_writeup(md_file, plataforma, resumen, nav_dict)

    # Mostrar resumen de lo procesado
    print("\n📋 RESUMEN DE IMPORTACIÓN:\n")
    for nombre, estado in resumen:
        print(f"🖹 {nombre:<30} {estado}")

    guardar_nav(nav_dict)
    print("🎉 Proceso finalizado.\n")

if __name__ == "__main__":
    main()
