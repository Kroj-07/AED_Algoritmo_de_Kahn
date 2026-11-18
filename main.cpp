#include "kahn_interface.hpp"
#include <iostream>
#include <string>

// Grafo de demo: 6 nodos, dos fuentes (0 y 5).
static Graph buildDemoGraph() {
    Graph g(6);
    g.addEdge(0, 1); g.addEdge(0, 2); g.addEdge(5, 2);
    g.addEdge(5, 4); g.addEdge(1, 3); g.addEdge(2, 3); g.addEdge(4, 3);
    return g;
}

// Mismo grafo + arista 3->0 que cierra un ciclo (0->1->3->0).
static Graph buildCycleGraph() {
    Graph g(6);
    g.addEdge(0, 1); g.addEdge(0, 2); g.addEdge(5, 2);
    g.addEdge(5, 4); g.addEdge(1, 3); g.addEdge(2, 3); g.addEdge(4, 3);
    g.addEdge(3, 0); // Cierra el ciclo
    return g;
}

static int runAndTrace(const Graph& g, const std::string& outPath) {
    TraceWriter tw(outPath);
    tw.setGraph(g.n, g.edges);
    KahnResult r = kahn(g, &tw);
    tw.flush();
    std::cout << "Traza escrita en: " << outPath << " (hasCycle: " << (r.hasCycle ? "true" : "false") << ")\n";
    return 0;
}

int main(int argc, char** argv) {
    std::string arg = (argc > 1) ? std::string(argv[1]) : "";

    // Si el argumento contiene "cycle", generamos el grafo con ciclo
    if (arg.find("cycle") != std::string::npos) {
        return runAndTrace(buildCycleGraph(), "trace_cycle.json");
    }

    // Si no, generamos el grafo normal
    std::string outPath = (argc > 1) ? arg : "trace.json";
    return runAndTrace(buildDemoGraph(), outPath);
}