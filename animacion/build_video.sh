#!/usr/bin/env bash
# Uso (desde cualquier carpeta): ./animacion/build_video.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUT="$SCRIPT_DIR/video"
mkdir -p "$OUT"

# 0) Dependencias
for cmd in g++ manim ffmpeg; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "ERROR: '$cmd' no está instalado o no está en el PATH."; exit 1; }
done

# 1) Compilar C++ y generar trazas
echo "Compilando C++..."
cd "$REPO_ROOT"
g++ -std=c++17 main.cpp graph.cpp int_queue.cpp kahn.cpp trace.cpp -o kahn.exe

echo "Generando archivos JSON..."
rm -f trace.json trace_cycle.json
./kahn.exe trace.json
./kahn.exe --cycle

for f in trace.json trace_cycle.json; do
  [ -s "$f" ] || { echo "ERROR: no se generó $f (¿antivirus / Smart App Control bloqueando kahn.exe?)"; exit 1; }
done

# 2) Copiar trazas junto a las escenas
cp trace.json trace_cycle.json "$SCRIPT_DIR/"

# 3) Renderizar escenas (Manim lee trace*.json con ruta relativa => estar en animacion/)
cd "$SCRIPT_DIR"
rm -rf "$OUT/videos"   # evita tomar MP4 viejos

echo "Renderizando escenas..."
render() { manim -qh --media_dir "$OUT" "$1" "$2"; }
render escenas_p1-p2.py Intro
render escenas_p1-p2.py Idea
render escenas_p3.py    Demo
render escenas_p3.py    CasoBorde
render escenas_p1-p2.py Complejidad
render escenas_p1-p2.py Creditos

# 4) Copiar y numerar
echo "Uniendo videos..."
copiar() {
  local src
  src="$(find "$OUT/videos" -path "*/1080p60/$1.mp4" | head -n 1)"
  [ -n "$src" ] || { echo "ERROR: no se encontró el render de $1"; exit 1; }
  cp "$src" "$OUT/$2"
}
copiar Intro        01_intro.mp4
copiar Idea         02_idea.mp4
copiar Demo         03_demo.mp4
copiar CasoBorde    04_caso_borde.mp4
copiar Complejidad  05_complejidad.mp4
copiar Creditos     06_creditos.mp4

cat > "$OUT/lista.txt" <<LISTA
file '01_intro.mp4'
file '02_idea.mp4'
file '03_demo.mp4'
file '04_caso_borde.mp4'
file '05_complejidad.mp4'
file '06_creditos.mp4'
LISTA

cd "$OUT"
ffmpeg -y -f concat -safe 0 -i lista.txt -c copy kahn_final.mp4 < /dev/null

rm -rf "$OUT/videos"
echo
echo "Listo. Video final en: $OUT/kahn_final.mp4"
