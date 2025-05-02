import os
import shutil
import sys
import re
import urllib.parse
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
EXPORT_DIR = ROOT / "notion_export"
WRITEUPS_DIR = ROOT / "Writeup-ctfs"
NAV_FILE = ROOT / "nav_generated.yml"

# Detecta hashes tipo: "Documento 19b360cb06dd800981cbd20c1e704239"
HASH_PATTERN = re.compile(r"\s[0-9a-f]{32}$", re.IGNORECASE)

def limpiar_hash(nombre: str) -> str:
    """Elimina el hash que Notion agrega al nombre del .md y de carpetas"""
    return HASH_PATTERN.sub("", nombre).strip()

def procesar_writeup(md_path: Path, plataforma: str, resumen: list, nav_dict: dict):
    nombre_md_original = md_path.stem
    base_name = limpiar_hash(nombre_md_original)

    plataforma_dir = WRITEUPS_DIR / plataforma
    imagenes_dir = plataforma_dir / "imagenes"
    imagenes_origen = md_path.parent / nombre_md_original  # carpeta con las imágenes

    md_dest = plataforma_dir / f"{base_name}.md"

    if md_dest.exists():
        resumen.append((base_name, "❌ Ya existe, omitido"))
        return

    content = md_path.read_text(encoding="utf-8")

    imagen_renombrada = {}

    # Renombrar y mover imágenes si hay
    if imagenes_origen.exists() and imagenes_origen.is_dir():
        for imagen in imagenes_origen.iterdir():
            nuevo_nombre = f"{base_name}_{imagen.name}"
            imagen_dest = imagenes_dir / nuevo_nombre
            imagenes_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(imagen), imagen_dest)
            imagen_renombrada[imagen.name] = nuevo_nombre

    # Reemplazo de rutas de imagen con verificación y marcador si falta
    def replace_img_path(match):
        alt_text = match.group(1)
        encoded_path = os.path.basename(match.group(2))
        original_path = urllib.parse.unquote(encoded_path)

        nuevo_path = imagen_renombrada.get(original_path)
        if nuevo_path:
            return f"![{alt_text}](./imagenes/{nuevo_path})"
        else:
            print(f"⚠️ Imagen no encontrada o no renombrada: {original_path}")
            return f"![{alt_text}]({match.group(2)}) <!-- IMAGEN NO RENOMBRADA: {original_path} -->"

    # Aplicar reemplazo a todo el contenido
    content = re.sub(r"!\[(.*?)\]\((.*?)\)", replace_img_path, content)

    # Escribir el nuevo archivo .md
    md_dest.parent.mkdir(parents=True, exist_ok=True)  # 👈 CREA la carpeta si no existe
    md_dest.write_text(content, encoding="utf-8")

    # Limpiar carpeta de imágenes original
    if imagenes_origen.exists():
        shutil.rmtree(imagenes_origen)

    # Eliminar archivo original
    md_path.unlink()

    resumen.append((base_name, "✅ Importado correctamente"))
    nav_dict[plataforma].append((base_name, f"Writeup-ctfs/{plataforma}/{base_name}.md"))

def guardar_nav(nav_dict: dict):
    with open(NAV_FILE, "w", encoding="utf-8") as f:
        f.write("nav:\n")
        for plataforma in sorted(nav_dict):
            f.write(f"  - {plataforma}:\n")
            for nombre, ruta in sorted(nav_dict[plataforma]):
                f.write(f"      - {nombre}: {ruta}\n")
    print(f"\n✅ Archivo actualizado: nav_generated.yml\n")

def main():
    if len(sys.argv) < 2:
        print("❌ Uso: python mover_writeup_notion.py <Plataforma>")
        sys.exit(1)

    plataforma = sys.argv[1]
    if not EXPORT_DIR.exists():
        print("❌ La carpeta 'notion_export/' no existe.")
        sys.exit(1)

    resumen = []
    nav_dict = defaultdict(list)

    for md_file in EXPORT_DIR.rglob("*.md"):
        procesar_writeup(md_file, plataforma, resumen, nav_dict)

    print("\n📋 RESUMEN DE IMPORTACIÓN:\n")
    for nombre, estado in resumen:
        print(f"🖹 {nombre:<30} {estado}")

    guardar_nav(nav_dict)
    print("🎉 Proceso finalizado.\n")

if __name__ == "__main__":
    main()