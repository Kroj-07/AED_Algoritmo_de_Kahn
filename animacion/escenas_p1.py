# escenas_p1.py  (P1: intro, complejidad y créditos)
# Render:  manim -pql escenas_p1.py Intro        (baja calidad, para probar)
#          manim -qh  escenas_p1.py Intro        (1080p, para el video final)
from manim import *

# ====== EDITA ESTO ======
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
