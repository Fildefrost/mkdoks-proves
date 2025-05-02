import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WRITEUPS_DIR = ROOT / "Writeup-ctfs"

def embellecer_cabecera(md_text: str, titulo: str) -> str:
    pattern = re.compile(
        r"Plataforma: (?P<plataforma>.+?)\s+OS: (?P<os>.+?)\s+Level: (?P<level>.+?)\s+Status: (?P<status>.+?)\s+Complete: (?P<complete>.+?)\s+EJPT: (?P<ejpt>.+?)\s+Created time: (?P<created>.+?)\s+IP: (?P<ip>[^\n]+)"
    )

    match = pattern.search(md_text)
    if not match:
        return f"# {titulo}\n\n---\n\n" + md_text

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

def procesar_existentes(force=False):
    total = 0
    actualizados = 0

    for plataforma_dir in WRITEUPS_DIR.iterdir():
        if not plataforma_dir.is_dir():
            continue

        for md_file in plataforma_dir.glob("*.md"):
            total += 1
            content = md_file.read_text(encoding="utf-8")

            if not force and content.lstrip().startswith("# "):
                continue

            title = md_file.stem
            updated = embellecer_cabecera(content, title)
            md_file.write_text(updated, encoding="utf-8")
            actualizados += 1
            print(f"✅ Cabecera aplicada a: {md_file}")

    print(f"\n🎯 Procesados: {total} archivos")
    print(f"🛠️ Cabeceras actualizadas: {actualizados}")

if __name__ == "__main__":
    force = "--force" in sys.argv
    procesar_existentes(force=force)
