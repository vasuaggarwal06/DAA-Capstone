"""Correctness tests: python -m unittest test_planner -v"""
import itertools, random, unittest
from sorting import merge_sort, quick_sort, heap_sort
from knapsack import knapsack
from graph import Graph, dijkstra, build_path, nearest_neighbor_tsp


class TestSorting(unittest.TestCase):
    def test_all_sorts_match_builtin(self):
        for _ in range(50):
            a = [random.randint(-50, 50) for _ in range(random.randint(0, 60))]
            for f in (merge_sort, quick_sort, heap_sort):
                self.assertEqual(f(a), sorted(a))

    def test_merge_sort_stable(self):
        a = [(1, "a"), (0, "b"), (1, "c"), (0, "d")]
        self.assertEqual(merge_sort(a, key=lambda x: x[0]),
                         [(0, "b"), (0, "d"), (1, "a"), (1, "c")])


class TestKnapsack(unittest.TestCase):
    def test_classic(self):
        best, idx, _ = knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7)
        self.assertEqual(best, 9)
        self.assertEqual(sum([1, 3, 4, 5][i] for i in idx) <= 7, True)

    def test_matches_brute_force(self):
        for _ in range(30):
            n = 8
            w = [random.randint(1, 10) for _ in range(n)]
            v = [random.randint(1, 50) for _ in range(n)]
            cap = random.randint(5, 30)
            brute = max(sum(v[i] for i in c)
                        for r in range(n + 1) for c in itertools.combinations(range(n), r)
                        if sum(w[i] for i in c) <= cap)
            self.assertEqual(knapsack(w, v, cap)[0], brute)


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.g = Graph()
        for u, v, w in [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)]:
            self.g.add_edge(u, v, w)

    def test_dijkstra(self):
        dist, prev = dijkstra(self.g, 0)
        self.assertEqual(dist, {0: 0, 1: 3, 2: 1, 3: 4})
        self.assertEqual(build_path(prev, 0, 3), [0, 2, 1, 3])

    def test_tsp_visits_all_and_returns(self):
        order, path, total = nearest_neighbor_tsp(self.g, 0, [1, 3])
        self.assertEqual(order[0], 0); self.assertEqual(order[-1], 0)
        self.assertEqual(set(order), {0, 1, 3})
        self.assertEqual(total, 8)   # 0->1 (3), 1->3 (1), 3->0 (4)


if __name__ == "__main__":
    unittest.main()
