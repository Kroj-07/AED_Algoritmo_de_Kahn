#!/usr/bin/env bash
set -e

# Rutas
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)" # .../animacion
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)" # raíz del repo
OUT="$SCRIPT_DIR/video" # animacion/video/
mkdir -p "$OUT"

# 1. Compilar y generar trazas desde la raíz
cd "$REPO_ROOT"
g++ -std=c++17 main.cpp graph.cpp int_queue.cpp kahn.cpp trace.cpp -o kahn
./kahn trace.json
./kahn --cycle # genera trace_cycle.json

# 2. Renderizar desde la carpeta animacion
cd "$SCRIPT_DIR"

# Copiar los JSON para que Manim los encuentre
cp "$REPO_ROOT/trace.json"        "$SCRIPT_DIR/trace.json"
cp "$REPO_ROOT/trace_cycle.json"  "$SCRIPT_DIR/trace_cycle.json" 2>/dev/null || true

# Renderizar las 6 escenas
echo "Renderizando escenas..."
manim -qh --media_dir "$OUT" escenas_p1-p2.py Intro
manim -qh --media_dir "$OUT" escenas_p1-p2.py Idea
manim -qh --media_dir "$OUT" escenas_p3.py    Demo
manim -qh --media_dir "$OUT" escenas_p3.py    CasoBorde
manim -qh --media_dir "$OUT" escenas_p1-p2.py Complejidad
manim -qh --media_dir "$OUT" escenas_p1-p2.py Creditos

# 3. Buscar los mp4 y copiarlos con nombres ordenados a la raíz de video/
find_mp4 () {
  find "$OUT" -path "*/1080p60/$1.mp4" | head -n 1
}

INTRO=$(find_mp4 Intro)
IDEA=$(find_mp4 Idea)
DEMO=$(find_mp4 Demo)
BORDE=$(find_mp4 CasoBorde)
COMP=$(find_mp4 Complejidad)
CRED=$(find_mp4 Creditos)

cp "$INTRO" "$OUT/01_intro.mp4"
cp "$IDEA"  "$OUT/02_idea.mp4"
cp "$DEMO"  "$OUT/03_demo.mp4"
cp "$BORDE" "$OUT/04_caso_borde.mp4"
cp "$COMP"  "$OUT/05_complejidad.mp4"
cp "$CRED"  "$OUT/06_creditos.mp4"

# 4. Crear lista y concatenar
cat > "$OUT/lista.txt" <<EOF
file '01_intro.mp4'
file '02_idea.mp4'
file '03_demo.mp4'
file '04_caso_borde.mp4'
file '05_complejidad.mp4'
file '06_creditos.mp4'
EOF

echo "Uniendo videos con ffmpeg..."
(cd "$OUT" && ffmpeg -y -f concat -safe 0 -i lista.txt -c copy kahn_final.mp4 < /dev/null)

# 5. Limpiar carpetas temporales de Manim
rm -rf "$OUT/videos"

echo "Ya está, video final en: $OUT/kahn_final.mp4"