#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUT="$SCRIPT_DIR/video"
mkdir -p "$OUT"

echo "Compilando C++..."
cd "$REPO_ROOT"
g++ -std=c++17 main.cpp graph.cpp int_queue.cpp kahn.cpp trace.cpp -o kahn.exe

echo "Generando archivos JSON..."
# Usamos winpty para asegurar que la ejecución del .exe no rompa Git Bash
cmd //c "kahn.exe trace.json"
cmd //c "kahn.exe --cycle"

if [ ! -f "trace.json" ]; then
    echo ""
    echo "ERROR: 'trace.json' no se creó."
    echo "Asegúrate de que Smart App Control (Seguridad de Windows) esté DESACTIVADO."
    exit 1
fi

echo "Preparando Manim..."
cd "$SCRIPT_DIR"
cp "$REPO_ROOT/trace.json"        "$SCRIPT_DIR/trace.json"
cp "$REPO_ROOT/trace_cycle.json"  "$SCRIPT_DIR/trace_cycle.json" 2>/dev/null || true

echo "Renderizando escenas..."
manim -qh --media_dir "$OUT" escenas_p1-p2.py Intro
manim -qh --media_dir "$OUT" escenas_p1-p2.py Idea
manim -qh --media_dir "$OUT" escenas_p3.py    Demo
manim -qh --media_dir "$OUT" escenas_p3.py    CasoBorde
manim -qh --media_dir "$OUT" escenas_p1-p2.py Complejidad
manim -qh --media_dir "$OUT" escenas_p1-p2.py Creditos

echo "Uniendo videos..."
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

cat > "$OUT/lista.txt" <<EOF
file '01_intro.mp4'
file '02_idea.mp4'
file '03_demo.mp4'
file '04_caso_borde.mp4'
file '05_complejidad.mp4'
file '06_creditos.mp4'
EOF

cd "$OUT"
ffmpeg -y -f concat -safe 0 -i lista.txt -c copy kahn_final.mp4 < /dev/null

rm -rf "$OUT/videos"
echo ""
echo "¡Ya está! Video final en: $OUT/kahn_final.mp4"