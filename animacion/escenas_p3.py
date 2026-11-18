import json
from manim import *

NOMBRES = {
    "P1": "Abigail Jaslin Cabanillas Ventocilla",
    "P2": "Kiara Luz Rojas Meza",
    "P3": "Azul Arbulú Silva",
}


class EscenaTemporizada(Scene):
    """Escena con duración objetivo (segundos) tomada del guion."""
    DURACION = 0

    def rellenar(self, reserva=0.0):
        """Espera lo que falte para llegar a DURACION.
        `reserva` = segundos de animaciones que aún faltan (p. ej. el FadeOut final)."""
        falta = self.DURACION - self.renderer.time - reserva
        if falta > 0.01:
            self.wait(falta)
        elif falta < -0.05:
            print(f"[AVISO] {type(self).__name__} se pasa {-falta:.1f}s de {self.DURACION}s")


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


def pintar(nodo, color):
    """Animación que colorea un nodo (círculo + relleno)."""
    return nodo[0].animate.set_color(color).set_fill(color, opacity=0.4)


class Demo(EscenaTemporizada):
    # Demostración caso normal, leyendo trace.json (guion: 1:15 - 2:25 = 70 s)
    DURACION = 70
    # Peso de cada tipo de evento: el tiempo sobrante se reparte proporcionalmente
    PESOS = {"init": 4, "pop": 2, "output": 2, "decrement": 2,
             "push": 2.5, "cycle": 2, "finish": 3}

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
        aristas_d = {}
        for u, v in trace["edges"]:
            a = Arrow(
                pos[u] + RIGHT * 0.45,
                pos[v] + LEFT * 0.45,
                buff=0.1,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15,
                )
            aristas.add(a)
            aristas_d[(u, v)] = a
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

        # Reproducir eventos: cada uno ocupa un "slot" proporcional a su peso
        eventos = trace["events"]
        total_pesos = sum(self.PESOS.get(e["type"], 2) for e in eventos)
        presupuesto = self.DURACION - self.renderer.time

        for ev in eventos:
            t = ev["type"]
            t0 = self.renderer.time
            slot = presupuesto * self.PESOS.get(t, 2) / total_pesos

            if t == "init":
                self.play(*[
                    Transform(grados[v], Text(f"in={g}", font_size=22, color=YELLOW).move_to(grados[v]))
                    for v, g in enumerate(ev["indegree"])
                ], run_time=1)
                self.actualizar_cola(cola_txt, ev["queue"])
                self.play(*[Indicate(nodos[v], color=GREEN) for v in ev["queue"]], run_time=1)
            elif t == "pop":
                self.actualizar_cola(cola_txt, ev["queue"])
                self.play(pintar(nodos[ev["node"]], YELLOW), run_time=0.5)
            elif t == "output":
                self.actualizar_orden(orden_txt, ev["order"])
                self.play(pintar(nodos[ev["node"]], GREEN), run_time=0.5)
            elif t == "decrement":
                v = ev["to"]
                nuevo = Text(f"in={ev['indegree']}", font_size=22, color=RED).move_to(grados[v])
                self.play(
                    Indicate(aristas_d[(ev["from"], v)], color=RED),
                    Transform(grados[v], nuevo),
                    run_time=0.8,
                )
            elif t == "push":
                self.actualizar_cola(cola_txt, ev["queue"])
                self.play(Indicate(nodos[ev["node"]], color=GREEN), run_time=0.8)
            elif t == "cycle":
                for v in ev["remaining"]:
                    self.play(nodos[v][0].animate.set_color(RED), run_time=0.2)

            # Completar el slot (si la animación fue más corta)
            falta = t0 + slot - self.renderer.time
            if falta > 0.01:
                self.wait(falta)

        self.rellenar()

    @staticmethod
    def actualizar_cola(txt, queue):
        nuevo = Text(str(queue), font_size=26, color=GREEN).move_to(txt)
        txt.become(nuevo)

    @staticmethod
    def actualizar_orden(txt, order):
        nuevo = Text(str(order), font_size=26, color=GREEN).move_to(txt)
        txt.become(nuevo)


class CasoBorde(EscenaTemporizada):
    # Caso borde: ciclo, leyendo trace_cycle.json (guion: 2:25 - 3:00 = 35 s)
    DURACION = 35

    def construct(self):
        trace = cargar_trace("trace_cycle.json")
        pos = posiciones_demo()
        n = trace["n"]
        eventos = trace["events"]
        orden_final = eventos[-1]["order"]

        titulo = Text("Caso borde: ciclo", font_size=44).to_edge(UP, buff=0.4)
        self.play(Write(titulo))

        nodos = {}
        for v, p in pos.items():
            c = Circle(radius=0.45, color=BLUE, fill_opacity=0.15).move_to(p)
            t = Text(str(v), font_size=34).move_to(p)
            nodos[v] = VGroup(c, t)
        self.play(*[FadeIn(nd) for nd in nodos.values()])

        aristas = VGroup()
        aristas_d = {}
        for u, v in trace["edges"]:
            color = RED if (u, v) == (3, 0) else WHITE  # arista del ciclo
            a = Arrow(
                pos[u] + RIGHT * 0.45,
                pos[v] + LEFT * 0.45,
                buff=0.1,
                stroke_width=3,
                color=color,
                max_tip_length_to_length_ratio=0.15,
                )
            aristas.add(a)
            aristas_d[(u, v)] = a
        self.play(*[GrowArrow(a) for a in aristas])

        # 1) La arista extra cierra el ciclo
        aviso = Text("La arista 3 -> 0 cierra el ciclo 0 -> 1 -> 3 -> 0",
                     font_size=28, color=RED).to_edge(DOWN, buff=0.8)
        self.play(Write(aviso))
        self.play(Indicate(aristas_d[(3, 0)], color=RED, scale_factor=1.3), run_time=1.5)
        self.wait(6)
        self.play(FadeOut(aviso))

        # 2) El algoritmo avanza mientras haya grado 0
        for ev in eventos:
            if ev["type"] == "output":
                self.play(pintar(nodos[ev["node"]], GREEN), run_time=0.6)
                self.wait(3)
            elif ev["type"] == "cycle":
                # 3) La cola se vacía con nodos sin procesar
                vacia = Text("La cola se vacía y quedan nodos sin procesar",
                             font_size=28).to_edge(DOWN, buff=0.8)
                self.play(Write(vacia))
                self.wait(5)
                self.play(*[pintar(nodos[v], RED) for v in ev["remaining"]], run_time=1)
                self.play(FadeOut(vacia))
                bloqueados = VGroup(
                    Text(f"Orden parcial: {orden_final} ({len(orden_final)} de {n} nodos)",
                         font_size=26),
                    Text("Nodos bloqueados: " + str(ev["remaining"]), font_size=30, color=RED),
                ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
                self.play(Write(bloqueados))
                break

        self.rellenar()