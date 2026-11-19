# Mini-Courier Planner (DAA Capstone, ETCCDA302)

Pipeline: **merge sort** (priority by deadline) -> **0/1 knapsack DP** (best parcels for one trip)
-> **Dijkstra** (shortest paths) -> **nearest-neighbor TSP** (overall delivery route).

## How to run (Python 3.8+, matplotlib only needed for benchmark/report)
    python generate_data.py                       # creates data/small, medium, large
    python main.py --data data/small --capacity 40
    python main.py --data data/large --capacity 2500
    python -m unittest test_planner -v            # correctness tests
    python benchmark.py                           # runtime table + results/runtime_chart.png

## Files
| File | Purpose |
|---|---|
| sorting.py | merge, quick, heap sort |
| knapsack.py | 0/1 knapsack (DP tabulation + backtracking) |
| graph.py | graph, Dijkstra (min-heap), nearest-neighbor TSP |
| data_io.py / generate_data.py | dataset CSV generation and loading |
| main.py | integrated planner |
| benchmark.py | timing and chart |
| test_planner.py | tests (sorts vs built-in, knapsack vs brute force, Dijkstra, TSP) |
| Capstone_Report.docx | final report |

## Data formats
parcels.csv: `id,weight,value,deadline,dest` | graph.csv: `u,v,distance` (node 0 = depot, undirected)
