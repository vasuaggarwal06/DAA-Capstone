"""Graph, Dijkstra's shortest path (Unit 3) and Nearest-Neighbor TSP approximation."""
import heapq


class Graph:
    """Undirected weighted graph stored as an adjacency list."""

    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v, w):
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, []).append((u, w))

    @property
    def nodes(self):
        return list(self.adj)


def dijkstra(graph, source):
    """Min-heap Dijkstra. Time O((V+E) log V). Returns (dist, prev)."""
    dist = {node: float("inf") for node in graph.adj}
    prev = {node: None for node in graph.adj}
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                      # stale entry
        for v, w in graph.adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def build_path(prev, source, target):
    """Rebuild source->target path from the prev map."""
    path, cur = [], target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == source else []


def nearest_neighbor_tsp(graph, depot, stops):
    """Greedy TSP approximation. Run Dijkstra from the depot and every stop,
    then repeatedly go to the closest unvisited stop, finally return to depot.
    Time O(k * (V+E) log V + k^2) for k stops.
    Returns (order, full_node_path, total_distance)."""
    stops = [s for s in dict.fromkeys(stops) if s != depot]
    sp = {n: dijkstra(graph, n) for n in [depot] + stops}   # (dist, prev) per node
    order, current, total = [depot], depot, 0
    remaining = set(stops)
    full_path = [depot]
    while remaining:
        nxt = min(remaining, key=lambda s: sp[current][0][s])
        total += sp[current][0][nxt]
        full_path += build_path(sp[current][1], current, nxt)[1:]
        order.append(nxt)
        remaining.remove(nxt)
        current = nxt
    total += sp[current][0][depot]                          # return to depot
    full_path += build_path(sp[current][1], current, depot)[1:]
    order.append(depot)
    return order, full_path, total
