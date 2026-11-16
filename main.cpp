// main.cpp
#include "kahn_interface.hpp"
#include "trace.cpp"
#include <iostream>

// Grafo de demo: 6 nodos, dos fuentes (0 y 5).
//   0 -> 1, 0 -> 2
//   5 -> 2, 5 -> 4
//   1 -> 3
//   2 -> 3
//   4 -> 3
//   3 -> (sin salida)

static Graph buildDemoGraph() {
    Graph g(6);

    g.addEdge(0, 1);
        g.addEdge(0, 2);
            g.addEdge(5, 2);
                g.addEdge(5, 4);
                    g.addEdge(1, 3);
                        g.addEdge(2, 3);
                            g.addEdge(4, 3);

    return g;
}

int main(int argc, char** argv) {
    std::string outPath = (argc > 1) ? argv[1]: "trace.json";

    Graph g = buildDemoGraph();
    TraceWriter tw(outPath);
    tw.setGraph(g.n, g.edges);

    KahnResult r = kahn(g, &tw);
    tw.flush();

    std::cout << "Orden topologico:";
    for (int v : r.order) std::cout << " " << v;
    std::cout << "\nhasCycle: " << (r.hasCycle ? "true" : "false") << "\n";
    std::cout << "Traza escrita en: " << outPath << "\n";

    // Comprobación mínima: si no hay ciclo, el orden debe tener n nodos.
    if (!r.hasCycle && (int)r.order.size() != g.n) {
        std::cerr << "[main] ERROR: orden incompleto sin ciclo detectado\n";
        return 1;
    }
    return 0;
}