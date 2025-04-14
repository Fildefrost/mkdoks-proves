import os

def get_title_from_path(path):
    # Usa el nombre del archivo o carpeta como título
    name = os.path.splitext(os.path.basename(path))[0]
    return name.replace('_', ' ').replace('-', ' ').title()

def build_nav(path, base=''):
    nav = []
    entries = sorted(os.listdir(path))
    for entry in entries:
        full_path = os.path.join(path, entry)
        rel_path = os.path.join(base, entry).replace("\\", "/")

        if os.path.isdir(full_path):
            # Es una subcarpeta: hacer recursivo
            sub_nav = build_nav(full_path, rel_path)
            nav.append({get_title_from_path(entry): sub_nav})
        elif entry.endswith('.md'):
            nav.append({get_title_from_path(entry): rel_path})
    return nav

def print_nav(nav, indent=2):
    spaces = '  ' * indent
    for item in nav:
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, list):
                    print(f"{spaces}- {key}:")
                    print_nav(value, indent + 1)
                else:
                    print(f"{spaces}- {key}: {value}")
        else:
            print(f"{spaces}- {item}")

# Ejecutar
print("nav:")
print_nav(build_nav("docs"))
