"""Runtime comparison for different input sizes -> results/runtime.csv, runtime_chart.png"""
import csv, time, random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sorting import merge_sort, quick_sort, heap_sort
from knapsack import knapsack
from graph import Graph, dijkstra, nearest_neighbor_tsp
from data_io import generate_dataset

SIZES = [10, 100, 500, 1000, 2000]


def timeit(fn):
    s = time.perf_counter(); r = fn(); return time.perf_counter() - s, r


rows = []
for n in SIZES:
    random.seed(1)
    parcels, edges = generate_dataset(n, max(8, n // 3))
    g = Graph()
    for u, v, w in edges:
        g.add_edge(u, v, w)
    key = lambda p: p["deadline"]
    r = {"n": n}
    r["merge_sort"], _ = timeit(lambda: merge_sort(parcels, key))
    r["quick_sort"], _ = timeit(lambda: quick_sort(parcels, key))
    r["heap_sort"], _ = timeit(lambda: heap_sort(parcels, key))
    cap = 5 * n  # capacity grows with n so ~half the parcels fit
    r["knapsack"], (_, idx, _) = timeit(lambda: knapsack([p["weight"] for p in parcels],
                                                         [p["value"] for p in parcels], cap))
    stops = [parcels[i]["dest"] for i in idx]
    r["dijkstra"], _ = timeit(lambda: dijkstra(g, 0))
    r["tsp"], _ = timeit(lambda: nearest_neighbor_tsp(g, 0, stops))
    rows.append(r)
    print({k: (round(v, 5) if k != "n" else v) for k, v in r.items()})

cols = ["n", "merge_sort", "quick_sort", "heap_sort", "knapsack", "dijkstra", "tsp"]
with open("results/runtime.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

fig, ax = plt.subplots(1, 2, figsize=(13, 5))
for c in ["merge_sort", "quick_sort", "heap_sort"]:
    ax[0].plot(SIZES, [r[c] for r in rows], marker="o", label=c)
ax[0].set_title("Sorting algorithms"); ax[0].legend()
for c in ["merge_sort", "knapsack", "dijkstra", "tsp"]:
    ax[1].plot(SIZES, [r[c] for r in rows], marker="o", label=c)
ax[1].set_title("Major steps of the planner"); ax[1].legend(); ax[1].set_yscale("log")
for a in ax:
    a.set_xlabel("number of parcels (n)"); a.set_ylabel("time (seconds)"); a.grid(alpha=.3)
plt.tight_layout(); plt.savefig("results/runtime_chart.png", dpi=150)
