# Guía para compilar y renderizar la animación en Windows

Esta guía detalla el proceso exacto para generar el video final 
(`kahn_final.mp4`) desde cero en un entorno _Windows_.

Requisitos previos:
- Tener instalado _Git_ (para usar Git Bash).
- Tener instalado _Python_ y _Manim_.
- Tener instalado _ffmpeg_.
- Compilador _g++ (MinGW)_.

---

0. Desactivar _Smart App Control_.

> Windows 11 cuenta con una política de seguridad que bloquea la ejecución 
> de archivos `.exe` no firmados. Si no se desactiva, el _script_ fallará silenciosamente y no generará los _JSON_.

   1. Abrir el menú Inicio y buscar "Seguridad de Windows".
   2. Ir a "Control de aplicaciones y navegador".
   3. Hacer clic en "Configuración del Control inteligente de aplicaciones".
   4. Cambiar la opción a "Desactivado".

1. Ejecutar el _script_ `build_video.sh` en _Git Bash_.

   1. Abrir _Git Bash_ en la raíz del proyecto.
   2. Dar permisos de ejecución al _script_: `chmod +x animacion/build_video.sh`
   3. Ejecutar el script: `./animacion/build_video.sh`.

> El renderizado de las 6 escenas puede tardar varios minutos, no necesariamente no funciona.

2. Revisa que funcione

    Una vez que la terminal haya terminado abrir el explorador de archivos y dirigirse a: `animacion/video/`.

    Ahí se deberían encontrarán los siguientes archivos:
      - 01_intro.mp4
      - 02_idea.mp4
      - 03_demo.mp4
      - 04_caso_borde.mp4
      - 05_complejidad.mp4
      - 06_creditos.mp4
      - kahn_final.mp4