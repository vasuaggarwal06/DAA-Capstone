"""Creates sample datasets in data/small, data/medium, data/large."""
import os
from data_io import generate_dataset, save_dataset

for name, p, n in [("small", 10, 8), ("medium", 100, 60), ("large", 1000, 400)]:
    os.makedirs(f"data/{name}", exist_ok=True)
    parcels, edges = generate_dataset(p, n)
    save_dataset(f"data/{name}", parcels, edges)
    print(f"data/{name}: {p} parcels, {n} nodes, {len(edges)} edges")
