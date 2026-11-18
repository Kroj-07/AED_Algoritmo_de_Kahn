import json
from manim import *

NOMBRES = {
    "P1": "Abigail Jaslin Cabanillas Ventocilla",
    "P2": "Kiara Luz Rojas Meza",
    "P3": "Azul Arbulú Silva",
}

def cargar_trace(path):
    with open(path, "r") as f:
        return json.load(f)

def posiciones_demo():
    # Grafo de 6 nodos: 0->1, 0->2, 5->2, 5->4, 1->3, 2->3, 4->3
    return {
        0: LEFT * 5 + UP * 2,
        5: LEFT * 5 + DOWN * 2,
        1: LEFT * 2 + UP * 2,
        2: LEFT * 2 + UP * 0,
        4: LEFT * 2 + DOWN * 2,
        3: RIGHT * 2 + UP * 0,
    }


class Demo(Scene):
    # Demostración caso normal, leyendo trace.json
    def construct(self):
        trace = cargar_trace("trace.json")
        pos = posiciones_demo()

        titulo = Text("Demostración paso a paso", font_size=44).to_edge(UP)
        self.play(Write(titulo))

        # Nodos
        nodos = {}
        for v, p in pos.items():
            c = Circle(radius=0.45, color=BLUE, fill_opacity=0.15).move_to(p)
            t = Text(str(v), font_size=34).move_to(p)
            nodos[v] = VGroup(c, t)
        self.play(*[FadeIn(n) for n in nodos.values()])

        # Aristas
        aristas = VGroup()
        for u, v in trace["edges"]:
            aristas.add(
                Arrow(
                    pos[u] + RIGHT * 0.45,
                    pos[v] + LEFT * 0.45,
                    buff=0.1,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.15,
                    )
            )
        self.play(*[GrowArrow(a) for a in aristas])

        # Etiquetas de grado
        grados = {}
        for v in range(trace["n"]):
            et = Text("in=?", font_size=22, color=YELLOW)
            et.next_to(pos[v], UP, buff=0.1)
            grados[v] = et
        self.play(*[FadeIn(g) for g in grados.values()])

        # Panel lateral: cola y orden
        cola_titulo = Text("Cola", font_size=28, color=GREEN).move_to(RIGHT * 5 + UP * 3)
        orden_titulo = Text("Orden", font_size=28, color=GREEN).move_to(RIGHT * 5 + UP * 1)
        cola_txt = Text("[ ]", font_size=26).next_to(cola_titulo, DOWN, buff=0.2)
        orden_txt = Text("[ ]", font_size=26).next_to(orden_titulo, DOWN, buff=0.2)
        self.play(Write(cola_titulo), Write(orden_titulo), FadeIn(cola_txt), FadeIn(orden_txt))

        # Reproducir eventos
        for ev in trace["events"]:
            t = ev["type"]
            if t == "init":
                for v, g in enumerate(ev["indegree"]):
                    nuevo = Text(f"in={g}", font_size=22, color=YELLOW).move_to(grados[v])
                    self.play(Transform(grados[v], nuevo), run_time=0.15)
                self.actualizar_cola(cola_txt, ev["queue"])
            elif t == "pop":
                self.actualizar_cola(cola_txt, ev["queue"])
            elif t == "output":
                self.actualizar_orden(orden_txt, ev["order"])
            elif t == "decrement":
                v = ev["to"]
                nuevo = Text(f"in={ev['indegree']}", font_size=22, color=RED).move_to(grados[v])
                self.play(Transform(grados[v], nuevo), run_time=0.2)
            elif t == "push":
                self.actualizar_cola(cola_txt, ev["queue"])
            elif t == "cycle":
                # Resaltar los que quedaron bloqueados
                for v in ev["remaining"]:
                    self.play(nodos[v][0].animate.set_color(RED), run_time=0.2)
            elif t == "finish":
                self.wait(1)

        self.wait(2)

    @staticmethod
    def actualizar_cola(txt, queue):
        nuevo = Text(str(queue), font_size=26, color=GREEN).move_to(txt)
        txt.become(nuevo)

    @staticmethod
    def actualizar_orden(txt, order):
        nuevo = Text(str(order), font_size=26, color=GREEN).move_to(txt)
        txt.become(nuevo)


class CasoBorde(Scene):
    # Caso borde: ciclo, leyendo trace_cycle.json
    def construct(self):
        trace = cargar_trace("trace_cycle.json")
        pos = posiciones_demo()

        titulo = Text("Caso borde: ciclo", font_size=44).to_edge(UP, buff=0.4)
        self.play(Write(titulo))

        nodos = {}
        for v, p in pos.items():
            c = Circle(radius=0.45, color=BLUE, fill_opacity=0.15).move_to(p)
            t = Text(str(v), font_size=34).move_to(p)
            nodos[v] = VGroup(c, t)
        self.play(*[FadeIn(n) for n in nodos.values()])

        aristas = VGroup()
        for u, v in trace["edges"]:
            color = RED if (u, v) == (3, 0) else WHITE  # arista del ciclo
            aristas.add(
                Arrow(
                    pos[u] + RIGHT * 0.45,
                    pos[v] + LEFT * 0.45,
                    buff=0.1,
                    stroke_width=3,
                    color=color,
                    max_tip_length_to_length_ratio=0.15,
                    )
            )
        self.play(*[GrowArrow(a) for a in aristas])

        for ev in trace["events"]:
            if ev["type"] == "cycle":
                for v in ev["remaining"]:
                    self.play(nodos[v][0].animate.set_color(RED), run_time=0.3)
                bloqueados = Text(
                    "Nodos bloqueados: " + str(ev["remaining"]),
                    font_size=30, color=RED,
                    ).to_edge(DOWN, buff=0.8)
                self.play(Write(bloqueados))
                break

        self.wait(2)