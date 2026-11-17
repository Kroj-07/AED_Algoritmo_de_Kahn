// graph.cpp  (P1)
#include "kahn_interface.hpp"
#include <stdexcept>

Graph::Graph(int n) : n(n), adj(n) {}

void Graph::addEdge(int u, int v) {
    if (u < 0 || u >= n || v < 0 || v >= n)
        throw std::out_of_range("addEdge: nodo fuera de rango");
    adj[u].push_back(v);
    edges.emplace_back(u, v);   // para exportar al JSON
}

std::vector<int> Graph::computeIndegree() const {
    std::vector<int> indeg(n, 0);
    for (int u = 0; u < n; ++u)
        for (int v : adj[u])
            ++indeg[v];
    return indeg;
}
