#include "kahn_interface.hpp"

KahnResult kahn(const Graph& g, TraceWriter* trace) {
    // 1) Grados de entrada iniciales ( P1)
    std::vector<int> indeg = g.computeIndegree();

    // 2) Cola inicial con todos los nodos de grado 0
    IntQueue q(g.n);
    for (int u = 0; u < g.n; ++u) {
        if (indeg[u] == 0) q.push(u);
    }

    if (trace) trace->init(indeg, q.snapshot());

    // 3) Bucle principal
    std::vector<int> order;
    order.reserve(g.n);

    while (!q.empty()) {
        int u = q.pop();
        if (trace) trace->pop(u, q.snapshot());       // queue DESPUÉS del pop

        order.push_back(u);
        if (trace) trace->output(u, order);           // order DESPUÉS del append

        for (int v : g.adj[u]) {
            --indeg[v];
            if (trace) trace->decrement(u, v, indeg[v]);

            if (indeg[v] == 0) {
                q.push(v);
                if (trace) trace->push(v, q.snapshot()); // queue DESPUÉS del push
            }
        }
    }

    // 4) Detección de ciclo y reporte final
    bool hasCycle = static_cast<int>(order.size()) < g.n;

    if (hasCycle && trace) {
        // Nodos que nunca salieron
        std::vector<bool> emitted(g.n, false);
        for (int u : order) emitted[u] = true;

        std::vector<int> remaining;
        for (int u = 0; u < g.n; ++u)
            if (!emitted[u]) remaining.push_back(u);

        trace->cycle(remaining);
    }

    if (trace) trace->finish(order, hasCycle);

    return KahnResult{order, hasCycle};
}