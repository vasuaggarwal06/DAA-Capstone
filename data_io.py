"""Dataset generation and loading (CSV files)."""
import csv
import random
from graph import Graph


def generate_dataset(n_parcels, n_nodes, seed=42):
    """Random connected graph (node 0 = depot) and random parcels."""
    rnd = random.Random(seed)
    edges = []
    for v in range(1, n_nodes):                       # spanning tree => connected
        edges.append((rnd.randrange(v), v, rnd.randint(2, 20)))
    for _ in range(2 * n_nodes):                      # extra edges
        u, v = rnd.sample(range(n_nodes), 2) if n_nodes > 1 else (0, 0)
        edges.append((u, v, rnd.randint(2, 20)))
    parcels = [{"id": f"P{i+1}", "weight": rnd.randint(1, 20),
                "value": rnd.randint(10, 100), "deadline": rnd.randint(1, 48),
                "dest": rnd.randrange(1, n_nodes)} for i in range(n_parcels)]
    return parcels, edges


def save_dataset(folder, parcels, edges):
    with open(f"{folder}/parcels.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "weight", "value", "deadline", "dest"])
        w.writeheader(); w.writerows(parcels)
    with open(f"{folder}/graph.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["u", "v", "distance"]); w.writerows(edges)


def load_parcels(path):
    with open(path) as f:
        return [{"id": r["id"], "weight": int(r["weight"]), "value": int(r["value"]),
                 "deadline": int(r["deadline"]), "dest": int(r["dest"])}
                for r in csv.DictReader(f)]


def load_graph(path):
    g = Graph()
    with open(path) as f:
        for r in csv.DictReader(f):
            g.add_edge(int(r["u"]), int(r["v"]), int(r["distance"]))
    return g
