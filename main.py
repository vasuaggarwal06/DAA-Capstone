"""Mini-Courier Planner: sort -> knapsack -> Dijkstra -> nearest-neighbor TSP.
Usage: python main.py [--data data/small] [--capacity 40]"""
import argparse
import time
from sorting import merge_sort
from knapsack import knapsack
from graph import dijkstra, nearest_neighbor_tsp
from data_io import load_parcels, load_graph


def plan(parcels, graph, capacity, verbose=True):
    t = {}
    # Phase 2a: prioritise parcels - earliest deadline first (merge sort, stable)
    s = time.perf_counter()
    ordered = merge_sort(parcels, key=lambda p: p["deadline"])
    t["sorting"] = time.perf_counter() - s
    # Phase 2b: 0/1 knapsack - best set of parcels for one trip
    s = time.perf_counter()
    best, idx, dp = knapsack([p["weight"] for p in ordered],
                             [p["value"] for p in ordered], capacity)
    t["knapsack"] = time.perf_counter() - s
    chosen = [ordered[i] for i in idx]
    stops = [p["dest"] for p in chosen]
    # Phase 3a: individual shortest paths from depot (Dijkstra)
    s = time.perf_counter()
    dist, prev = dijkstra(graph, 0)
    t["dijkstra"] = time.perf_counter() - s
    # Phase 3b: overall route (nearest-neighbor TSP)
    s = time.perf_counter()
    order, path, total = nearest_neighbor_tsp(graph, 0, stops)
    t["tsp"] = time.perf_counter() - s
    if verbose:
        print("=== Parcels sorted by deadline (merge sort) ===")
        for p in ordered:
            print(f"  {p['id']:>5} deadline={p['deadline']:>2}h weight={p['weight']:>2} "
                  f"value={p['value']:>3} dest=node {p['dest']}")
        print(f"\n=== Knapsack (capacity {capacity}) ===")
        print(f"  Best total value : {best}")
        print(f"  Total weight     : {sum(p['weight'] for p in chosen)}")
        print("  Selected parcels :", ", ".join(p["id"] for p in chosen))
        print("\n=== Shortest distance from depot (Dijkstra) ===")
        for d in sorted(set(stops)):
            print(f"  depot -> node {d}: {dist[d]}")
        print("\n=== Delivery route (nearest-neighbor TSP) ===")
        print("  Stop order :", " -> ".join(map(str, order)))
        print("  Full path  :", " -> ".join(map(str, path)))
        print(f"  Route length: {total}")
        print("\n=== Runtime (seconds) ===")
        for k, v in t.items():
            print(f"  {k:<9}: {v:.6f}")
    return {"selected": chosen, "value": best, "order": order, "path": path,
            "length": total, "times": t}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/small")
    ap.add_argument("--capacity", type=int, default=40)
    a = ap.parse_args()
    plan(load_parcels(f"{a.data}/parcels.csv"), load_graph(f"{a.data}/graph.csv"), a.capacity)
