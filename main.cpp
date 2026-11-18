#include "kahn_interface.hpp"
#include <iostream>
#include <string>
#include <cstring>

// Grafo de demo: 6 nodos, dos fuentes (0 y 5).
//   0 -> 1, 0 -> 2
//   5 -> 2, 5 -> 4
//   1 -> 3
//   2 -> 3
//   4 -> 3

static Graph buildDemoGraph() { Graph g(6);
    g.addEdge(0, 1);
        g.addEdge(0, 2);
            g.addEdge(5, 2);
                g.addEdge(5, 4);
                    g.addEdge(1, 3);
                        g.addEdge(2, 3);
                            g.addEdge(4, 3);
    return g;
}

// Mismo grafo + arista 3->0 que cierra un ciclo (0->1->3->0).
static Graph buildCycleGraph() { Graph g(6);
    g.addEdge(0, 1);
        g.addEdge(0, 2);
            g.addEdge(5, 2);
                g.addEdge(5, 4);
                    g.addEdge(1, 3);
                        g.addEdge(2, 3);
                            g.addEdge(4, 3);
                                g.addEdge(3, 0);
    return g;
}

// Ejecuta kahn() sobre g, escribe la traza en outPath y reporta por stdout.
static int runAndTrace(const Graph& g, const std::string& outPath) {
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

int main(int argc, char** argv) {
    // Pasamos el argumento a std::string para evitar problemas con caracteres basura de Windows
    std::string arg1 = (argc > 1) ? std::string(argv[1]) : "";

    // Modo --cycle: si el argumento contiene "cycle", generamos el ciclo
    if (arg1.find("cycle") != std::string::npos) {
        Graph g = buildCycleGraph();
        return runAndTrace(g, "trace_cycle.json");
    }

    // Modo normal: grafo de demo sin ciclo.
    std::string outPath = (argc > 1) ? arg1 : "trace.json";
    Graph g = buildDemoGraph();
    return runAndTrace(g, outPath);
}