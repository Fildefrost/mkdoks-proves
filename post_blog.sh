#!/bin/bash

# Título de la entrada
TITLE="$1"
# Fecha actual
DATE=$(date +%Y-%m-%d)
# URL base de tu sitio
BASE_URL="https://fildefrost.github.io/"
# Generación del nombre del archivo en formato "fecha-titulo.md"
FILENAME="docs/blog/${TITLE// /-}.md"
# Enlace público para compartir en cualquier plataforma
PUBLIC_URL="${BASE_URL}$(echo $TITLE | tr '[:space:]' '-').html"
# Crear el archivo .md con la plantilla
cat > "$FILENAME" << EOF
---
title: "$TITLE"
date: $DATE
tags:
  - ejemplo
summary: >
  Breve resumen de la entrada.
---

# $TITLE

📅 Publicado el: **$DATE**

---

## 🗒️ Introducción

Primera nota publicada en el blog

---

## 📢 Comparte esta entrada

<!-- Botón de copiar -->
<button onclick="copyToClipboard()">Compartir nota</button>

<script> function copyToClipboard() { const el = document.createElement('textarea'); el.value = "$PUBLIC_URL"; document.body.appendChild(el); el.select(); document.execCommand('copy'); document.body.removeChild(el); alert('URL copiada al portapapeles: ' + el.value); } </script>
