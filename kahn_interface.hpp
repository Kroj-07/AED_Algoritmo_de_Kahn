// kahn_interface.hpp
// CONTRATO entre los 3 módulos. No cambiar firmas sin avisar a los otros dos.
//
//   P1 -> Graph, IntQueue            (graph.cpp, int_queue.cpp)
//   P2 -> kahn()                     (kahn.cpp)
//   P3 -> TraceWriter + main + tests (trace.cpp, main.cpp, tests.cpp)
#pragma once
#include <string>
#include <vector>

// ============================================================
// P1: estructuras base
// ============================================================
struct Graph {
    int n;                              // nodos 0..n-1
    std::vector<std::vector<int>> adj;  // adj[u] = lista de v con arista u->v
    std::vector<std::pair<int,int>> edges; // para exportar al JSON

    explicit Graph(int n);
    void addEdge(int u, int v);
    std::vector<int> computeIndegree() const; // grado de entrada de cada nodo
};

// Cola propia (arreglo circular). Cada nodo entra una sola vez => capacidad n basta.
class IntQueue {
public:
    explicit IntQueue(int capacity);
    void push(int x);
    int  pop();
    int  front() const;
    bool empty() const;
    int  size() const;
    std::vector<int> snapshot() const;  // frente -> fondo, para la traza
};

// ============================================================
// P3: traza (la animación SOLO lee lo que esto escribe)
// ============================================================
class TraceWriter {
public:
    explicit TraceWriter(const Graph& g);

    // Llamadas que hace kahn() en este orden:
    void init(const std::vector<int>& indeg, const std::vector<int>& queue);
    void pop(int node, const std::vector<int>& queue);
    void output(int node, const std::vector<int>& order);
    void decrement(int from, int to, int newIndeg);
    void push(int node, const std::vector<int>& queue);
    void cycle(const std::vector<int>& remaining); // nodos que nunca salieron
    void finish(const std::vector<int>& order, bool hasCycle);

    bool save(const std::string& path) const;       // escribe el JSON
};

// ============================================================
// P2: núcleo del algoritmo
// ============================================================
struct KahnResult {
    std::vector<int> order;  // orden topológico (parcial si hay ciclo)
    bool hasCycle;           // true si order.size() < g.n
};

// trace puede ser nullptr (para tests sin animación).
KahnResult kahn(const Graph& g, TraceWriter* trace = nullptr);

// Orden de eventos por iteración dentro de kahn():
//   init -> { pop -> output -> { decrement -> (push si llega a 0) }* }* -> (cycle?) -> finish

/* ============================================================
   FORMATO DEL JSON (trace.json) que lee la animación
   ============================================================
{
  "n": 5,
  "edges": [[0,1],[0,2],[1,3],[2,3],[3,4]],
  "events": [
    {"type":"init",      "indegree":[0,1,1,2,1], "queue":[0]},
    {"type":"pop",       "node":0, "queue":[]},
    {"type":"output",    "node":0, "order":[0]},
    {"type":"decrement", "from":0, "to":1, "indegree":0},
    {"type":"push",      "node":1, "queue":[1]},
    {"type":"decrement", "from":0, "to":2, "indegree":0},
    {"type":"push",      "node":2, "queue":[1,2]},
    ...
    {"type":"cycle",     "remaining":[3,4]},      // solo si hay ciclo
    {"type":"finish",    "order":[0,1,2,3,4], "hasCycle":false}
  ]
}
   Lectura en Python (para Manim):
     import json; t = json.load(open("trace.json"))
     for ev in t["events"]: ...   # una animación por evento
   ============================================================ */
