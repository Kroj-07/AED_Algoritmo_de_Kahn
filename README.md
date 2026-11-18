# [CS2023] Proyecto II: Algoritmo de Kahn (Topological sort)

**Estructura de datos:** _Algoritmo de Kahn (Topological sort)_.
**Curso:** CS2023 - Algoritmos y Estructuras de Datos (2026-2)
**Docente:** Víctor Racsó Galván Oyola

**Integrantes**:

|Nombre|Código|
|:----:|:----:|
| Abigail Jaslin Cabanillas Ventocilla | 202510438 |
| Azul Arbulú Silva | 202510303 |
| Kiara Luz Rojas Meza | 202510620 |

## Descripción del proyecto

Implementación en _C++17_ del **algoritmo de Kahn** para ordenamiento
topológico de un grafo dirigido, junto con una animación hecha en
**Manim** que reproduce paso a paso la ejecución real del algoritmo.

El proyecto está dividido en tres módulos independientes que se
comunican mediante `kahn_interface.hpp`:

| Módulo | Archivos | Responsable | Contenido |
|:------:|:--------:|:-----------:|:---------:|
| Estructuras base | `graph.cpp`, `int_queue.cpp` | Abigail Jaslin Cabanillas Ventocilla | `Graph` (listas de adyacencia), `IntQueue` (cola circular propia). |
| Núcleo del algoritmo | `kahn.cpp` | Kiara Luz Rojas Meza | `kahn()`: bucle principal, reducción de grados, detección de ciclo. |
| Traza y pruebas | `trace.cpp`, `main.cpp`, `tests.cpp` | Azul Arbulú Silva | `TraceWriter` (JSON), driver `main` y tests de casos borde. |

La animación **solo lee** el archivo `trace.json` generado por
`TraceWriter`; no recalcula nada. Así se garantiza que el video
muestra la ejecución real del código y no una simulación aparte.

## Requisitos del proyecto

+ Compilador con soporte de **C++17** (`g++` $\geq 7$, `clang++` $\geq 5$, MSVC $\geq 2017$).

+ **Python 3.9+** con `manim` instalado (para renderizar la animación).

+ `ffmpeg`: Manim lo usa internamente para producir el `.mp4`.

Instalación de Manim (una sola vez):

```bash
pip install manim
```

## Procedimiento de compilación y ejecución de pruebas

+ 1. Compilar todo el proyecto: `g++ -std=c++17 *.cpp -o kahn`.

+ 2. Ejecutar el driver: genera `trace.json` con el grafo de demo.

+ 3. Ejecutar los tests de casos borde:

    ```
    g++ -std=c++17 tests.cpp trace.cpp kahn.cpp graph.cpp int_queue.cpp -o tests
    ./tests
    ```

    + La salida esperada de `tests.cpp` es la siguiente:

    ```
    [test] vacio
    [test] un nodo
    [test] ciclo
    [test] varios grados 0
    [test] trace nullptr
    [test] traza JSON
    TODOS LOS TESTS PASARON
    ```

## Procedimiento para generar animación

+ 1. Generar la traza real (requiere haber compilado antes): `./kahn trace.json`.

+ 2. Renderizar la animación de Manim, Para renderizar la animación, desde el directiorio que contiene `animacion.py` correr:

    ```bash
    manim -pqh animacion.py KahnScene
    ```

    >El video no se rendizará si _Manim_ no está instalado, para verificar ello correr:
    >
    >```bash
    >manim --version
    >```

## Estructura resultante del repositorio 

```
AED_Algoritmo_de_Kahn/
├── animacion/
│   ├── escenas_p1-p2.py
│   ├── escenas_p3.py
│   ├── build_video.sh
│   ├── trace.json
│   ├── trace_cycle.json
│   └── video/
│       ├── 01_intro.mp4
│       ├── 02_idea.mp4
│       ├── 03_demo.mp4
│       ├── 04_caso_borde.mp4
│       ├── 05_complejidad.mp4
│       ├── 06_creditos.mp4
│       ├── kahn_final.mp4
│       └── lista.txt
├── informe/
│   ├── main.tex
│   └── Algoritmos_y_Estructuras_de_Datos___Informe_Proyecto_2.pdf
├── .gitignore
├── README.md
├── main.cpp
├── graph.cpp
├── int_queue.cpp
├── kahn.cpp
├── tests.cpp
├── trace.cpp
└── kahn_interface.hpp
```

## Video y repositorio

...

- Repositorio: [enlace a este repositorio](https://github.com/Kroj-07/AED_Algoritmo_de_Kahn.git)