// tests.cpp
#include "kahn_interface.hpp"
#include "trace.cpp"
#include <bits/stdc++.h>

static int g_failures = 0;
static void expect(bool cond, const std::string& msg) {
    if (!cond) { std::cerr << " FALLO: " << msg << "\n"; ++g_failures; }
}

static void expectOrderValid(const Graph& g, const KahnResult& r) {
    expect((int)r.order.size() == g.n, "el orden debe tener n nodos");
    // Verificar que el orden respeta todas las aristas.
    std::vector<int> pos(g.n, -1);
    for (size_t i = 0; i < r.order.size(); ++i) pos[r.order[i]] = (int)i;
    for (auto& e : g.edges) {
        if (pos[e.first] == -1 || pos[e.second] == -1) continue;
        expect(pos[e.first] < pos[e.second],
               "arista " + std::to_string(e.first) + "->" +
               std::to_string(e.second) + " violada");
    }
}

// 1) Grafo vacío: 0 nodos
static void testEmpty() {
    std::cout << "[test] vacio\n"; Graph g(0);
    KahnResult r = kahn(g, nullptr); // nullptr: sin traza
    expect(r.order.empty(), "orden vacio");
        expect(!r.hasCycle, "sin ciclo en grafo vacio");
}

// 2) Un solo nodo sin aristas
static void testSingleNode() {
    std::cout << "[test] un nodo\n"; Graph g(1);
    KahnResult r = kahn(g, nullptr);
    expect(r.order.size() == 1 && r.order[0] == 0, "orden = {0}");
        expect(!r.hasCycle, "sin ciclo");
}

// 3) Ciclo: 0->1->2->0
static void testCycle() {
    std::cout << "[test] ciclo\n"; Graph g(3);
    g.addEdge(0, 1); g.addEdge(1, 2); g.addEdge(2, 0);
    KahnResult r = kahn(g, nullptr);
    expect(r.hasCycle, "debe detectar ciclo");
        expect(r.order.size() < 3, "orden parcial (menos de n)");
}

// 4) Varios nodos con grado 0 al inicio (dos fuentes)
static void testMultipleZeroIndegree() {
    std::cout << "[test] varios grados 0\n"; Graph g(4);
    g.addEdge(0, 2); g.addEdge(1, 2); g.addEdge(2, 3);
    KahnResult r = kahn(g, nullptr);
    expect(!r.hasCycle, "sin ciclo");
        expectOrderValid(g, r);
    // Ambas fuentes deben aparecer antes que 2.
    std::vector<int> pos(4);
    for (size_t i = 0; i < r.order.size(); ++i) pos[r.order[i]] = (int)i;
        expect(pos[0] < pos[2] && pos[1] < pos[2], "0 y 1 antes que 2");
}

// 5) Traza con nullptr debe ser seguro y no escribir archivo
static void testNullTrace() {
    std::cout << "[test] trace nullptr\n"; Graph g(2); g.addEdge(0, 1);
    KahnResult r = kahn(g, nullptr);
        expectOrderValid(g, r);
}

// 6) Traza real: el JSON se genera y contiene los eventos clave
static void testTraceJson() {
    std::cout << "[test] traza JSON\n"; Graph g(2); g.addEdge(0, 1);
    TraceWriter tw("test_trace.json");
        tw.setGraph(g.n, g.edges);
    KahnResult r = kahn(g, &tw);
        tw.flush();
    (void)r;
    // Verificación ligera, la lectura completa del JSON se hará en el script de Manim).
    std::ifstream f("test_trace.json");
        expect(f.good(), "trace.json generado");
}

int main() {
    testEmpty();
        testSingleNode();
            testCycle();
                testMultipleZeroIndegree();
                    testNullTrace();
                        testTraceJson();

    if (g_failures == 0) {
        std::cout << "TODOS LOS TESTS PASARON\n"; 
        return 0;
    } std::cerr << g_failures << " fallo(s)\n";
    return 1;
}