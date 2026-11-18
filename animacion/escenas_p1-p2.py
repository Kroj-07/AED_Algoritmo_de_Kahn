from manim import *

NOMBRES = {
    "P1": "Abigail Jaslin Cabanillas Ventocilla",
    "P2": "Kiara Luz Rojas Meza",
    "P3": "Azul Arbulú Silva",
}

CURSO = "Algoritmos y Estructuras de Datos"
REPO = "https://github.com/Kroj-07/AED_Algoritmo_de_Kahn"


def caja(texto, color=BLUE, size=30):
    t = Text(texto, font_size=size)
    r = RoundedRectangle(
        corner_radius=0.15, width=t.width + 0.6, height=t.height + 0.5, color=color
    ).move_to(t)
    return VGroup(r, t)


class Intro(Scene):
    def construct(self):
        titulo = Text("Algoritmo de Kahn", font_size=64)
        sub = Text("Ordenamiento topológico", font_size=32, color=GRAY_B)
        sub.next_to(titulo, DOWN)
        self.play(Write(titulo))
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(1.5)
        self.play(FadeOut(titulo), FadeOut(sub))

        # Ejemplo cotidiano: tareas con dependencias
        medias = caja("Ponerse las medias").shift(LEFT * 3.5)
        zapatos = caja("Ponerse los zapatos", color=GREEN).shift(RIGHT * 3.5)
        flecha = Arrow(medias.get_right(), zapatos.get_left(), buff=0.15)
        self.play(FadeIn(medias), FadeIn(zapatos))
        self.play(GrowArrow(flecha))
        self.wait(1)

        pregunta = Text("¿En qué orden hacemos todas las tareas?", font_size=36)
        pregunta.to_edge(DOWN, buff=1)
        self.play(Write(pregunta))
        self.wait(2)
        self.play(FadeOut(VGroup(medias, zapatos, flecha, pregunta)))

class Idea(Scene):
    def construct(self):
        titulo = Text("¿Cómo funciona?", font_size=52).to_edge(UP)
        self.play(Write(titulo))

        # Grafo pequeño: 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
        # Posiciones fijas
        pos = {
            0: LEFT * 4 + UP * 1.5,
            1: LEFT * 1 + UP * 2.5,
            2: LEFT * 1 + UP * 0.5,
            3: RIGHT * 2 + UP * 1.5,
        }
        nodos = VGroup()
        for v, p in pos.items():
            c = Circle(radius=0.4, color=BLUE, fill_opacity=0.15).move_to(p)
            t = Text(str(v), font_size=32).move_to(p)
            nodos.add(VGroup(c, t))

        aristas = VGroup()
        for u, v in [(0, 1), (0, 2), (1, 3), (2, 3)]:
            aristas.add(
                Arrow(
                    pos[u] + RIGHT * 0.4,
                    pos[v] + LEFT * 0.4,
                    buff=0.1,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.15,
                    )
            )

        self.play(FadeIn(nodos), GrowArrow(aristas[0]))
        self.play(GrowArrow(aristas[1]))
        self.play(GrowArrow(aristas[2]), GrowArrow(aristas[3]))
        self.wait(0.5)

        # Grados de entrada sobre cada nodo
        grados = {0: 0, 1: 1, 2: 1, 3: 2}
        etiquetas_grado = VGroup()
        for v, g in grados.items():
            et = Text(f"in={g}", font_size=24, color=YELLOW)
            et.next_to(pos[v], UP, buff=0.1)
            etiquetas_grado.add(et)
        self.play(FadeIn(etiquetas_grado))
        self.wait(0.5)

        # Cola y Orden a la derecha
        cola_titulo = Text("Cola", font_size=30, color=GREEN).move_to(RIGHT * 5 + UP * 2)
        orden_titulo = Text("Orden", font_size=30, color=GREEN).move_to(RIGHT * 5 + UP * 0)
        self.play(Write(cola_titulo), Write(orden_titulo))

        cola_vacia = Text("[ ]", font_size=30).next_to(cola_titulo, DOWN, buff=0.2)
        orden_vacio = Text("[ ]", font_size=30).next_to(orden_titulo, DOWN, buff=0.2)
        self.play(FadeIn(cola_vacia), FadeIn(orden_vacio))

        # Paso 1: meter los de grado 0 (nodo 0)
        cola1 = Text("[0]", font_size=30, color=GREEN).move_to(cola_vacia)
        self.play(Transform(cola_vacia, cola1))
        self.wait(0.5)

        # Paso 2: sacar 0, agregarlo al orden, bajar grados de 1 y 2
        orden1 = Text("[0]", font_size=30, color=GREEN).move_to(orden_vacio)
        self.play(Transform(orden_vacio, orden1))
        cola2 = Text("[1]", font_size=30, color=GREEN).move_to(cola_vacia)
        self.play(Transform(cola_vacia, cola2))

        g1 = Text("in=0", font_size=24, color=RED).move_to(etiquetas_grado[1])
        g2 = Text("in=0", font_size=24, color=RED).move_to(etiquetas_grado[2])
        self.play(Transform(etiquetas_grado[1], g1), Transform(etiquetas_grado[2], g2))
        self.wait(0.5)

        cola3 = Text("[1, 2]", font_size=30, color=GREEN).move_to(cola_vacia)
        self.play(Transform(cola_vacia, cola3))
        self.wait(0.5)

        # Paso 3: terminar el 1, bajar grado de 3
        orden2 = Text("[0, 1]", font_size=30, color=GREEN).move_to(orden_vacio)
        self.play(Transform(orden_vacio, orden2))
        cola4 = Text("[2]", font_size=30, color=GREEN).move_to(cola_vacia)
        self.play(Transform(cola_vacia, cola4))
        g3 = Text("in=1", font_size=24, color=RED).move_to(etiquetas_grado[3])
        self.play(Transform(etiquetas_grado[3], g3))
        self.wait(0.5)

        # Paso 4: terminar 2, bajar 3 a 0, entrar a cola
        orden3 = Text("[0, 1, 2]", font_size=30, color=GREEN).move_to(orden_vacio)
        self.play(Transform(orden_vacio, orden3))
        g3b = Text("in=0", font_size=24, color=RED).move_to(etiquetas_grado[3])
        self.play(Transform(etiquetas_grado[3], g3b))
        cola5 = Text("[3]", font_size=30, color=GREEN).move_to(cola_vacia)
        self.play(Transform(cola_vacia, cola5))
        self.wait(0.5)

        # Paso 5: terminar 3, cola vacía, orden completo
        orden4 = Text("[0, 1, 2, 3]", font_size=30, color=GREEN).move_to(orden_vacio)
        self.play(Transform(orden_vacio, orden4))
        cola6 = Text("[ ]", font_size=30, color=GREEN).move_to(cola_vacia)
        self.play(Transform(cola_vacia, cola6))
        self.wait(2)

        self.play(
            FadeOut(
                VGroup(
                    titulo, nodos, aristas, etiquetas_grado,
                    cola_titulo, orden_titulo, cola_vacia, orden_vacio,
                )
            )
        )

class Complejidad(Scene):
    def construct(self):
        titulo = Text("Complejidad", font_size=52).to_edge(UP)
        self.play(Write(titulo))

        filas = [
            ("Calcular grados de entrada", "O(V + E)"),
            ("Cada nodo entra y sale de la cola", "O(V)"),
            ("Cada arista se revisa una vez", "O(E)"),
        ]
        grupo = VGroup()
        for i, (paso, costo) in enumerate(filas):
            y = 1.5 - i * 1.1
            izq = Text(paso, font_size=30).move_to([0, y, 0])
            izq.align_to([-6.5, 0, 0], LEFT)
            der = Text(costo, font_size=34, color=YELLOW).move_to([4.8, y, 0])
            fila = VGroup(izq, der)
            grupo.add(fila)
            self.play(FadeIn(fila, shift=RIGHT * 0.3))
            self.wait(1)

        total = Text("Tiempo total: O(V + E)", font_size=44, color=GREEN)
        total.move_to([0, -1.8, 0])
        memoria = Text("Memoria extra: O(V)", font_size=34)
        memoria.next_to(total, DOWN, buff=0.4)
        self.play(Write(total))
        self.wait(1)
        self.play(FadeIn(memoria))
        self.wait(3)
        self.play(FadeOut(VGroup(titulo, grupo, total, memoria)))


class Creditos(Scene):
    def construct(self):
        titulo = Text("Créditos", font_size=52).to_edge(UP)
        self.play(Write(titulo))

        roles = [
            ("P1", "Graph, IntQueue, guion e intro/complejidad/créditos"),
            ("P2", "Núcleo del algoritmo: kahn()"),
            ("P3", "Traza JSON, pruebas y escenas de la demo"),
        ]
        lineas = VGroup()
        for clave, rol in roles:
            nombre = Text(NOMBRES[clave], font_size=34, color=YELLOW)
            desc = Text(rol, font_size=26, color=GRAY_B)
            lineas.add(VGroup(nombre, desc).arrange(DOWN, buff=0.12))
        lineas.arrange(DOWN, buff=0.5).next_to(titulo, DOWN, buff=0.7)
        for l in lineas:
            self.play(FadeIn(l, shift=UP * 0.2))
            self.wait(0.8)

        pie = VGroup(
            Text(CURSO, font_size=26),
            Text(REPO, font_size=22, color=BLUE),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(pie))
        self.wait(3)
        self.play(FadeOut(VGroup(titulo, lineas, pie)))
