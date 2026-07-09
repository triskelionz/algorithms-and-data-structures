import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graphs.graph import Graph, bfs, dfs, dijkstra, shortest_path


def build_sample_graph() -> Graph:
    """A -> B -> D, A -> C -> D, with weights chosen so the shortest
    A -> D path goes through C, not through B.
    """
    graph = Graph()
    graph.add_edge("A", "B", weight=1)
    graph.add_edge("B", "D", weight=5)
    graph.add_edge("A", "C", weight=2)
    graph.add_edge("C", "D", weight=2)
    return graph


class TestGraph(unittest.TestCase):
    def test_add_edge_creates_both_nodes(self):
        graph = Graph()
        graph.add_edge("X", "Y")
        self.assertIn("X", graph.nodes)
        self.assertIn("Y", graph.nodes)

    def test_bidirectional_edge_adds_both_directions(self):
        graph = Graph()
        graph.add_edge("X", "Y", bidirectional=True)
        self.assertEqual([n for n, _ in graph.neighbors("Y")], ["X"])


class TestBFS(unittest.TestCase):
    def test_visits_every_reachable_node(self):
        graph = build_sample_graph()
        order = bfs(graph, "A")
        self.assertEqual(set(order), {"A", "B", "C", "D"})
        self.assertEqual(order[0], "A")

    def test_unknown_start_returns_empty(self):
        graph = build_sample_graph()
        self.assertEqual(bfs(graph, "Z"), [])

    def test_disconnected_node_not_visited(self):
        graph = build_sample_graph()
        graph.add_node("E")
        order = bfs(graph, "A")
        self.assertNotIn("E", order)


class TestDFS(unittest.TestCase):
    def test_visits_every_reachable_node(self):
        graph = build_sample_graph()
        order = dfs(graph, "A")
        self.assertEqual(set(order), {"A", "B", "C", "D"})
        self.assertEqual(order[0], "A")

    def test_single_node_graph(self):
        graph = Graph()
        graph.add_node("only")
        self.assertEqual(dfs(graph, "only"), ["only"])


class TestDijkstra(unittest.TestCase):
    def test_shortest_distances(self):
        graph = build_sample_graph()
        distances = dijkstra(graph, "A")
        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 1)
        self.assertEqual(distances["C"], 2)
        self.assertEqual(distances["D"], 4)  # via C (2 + 2), not via B (1 + 5)

    def test_unreachable_node_is_omitted(self):
        graph = build_sample_graph()
        graph.add_node("isolated")
        distances = dijkstra(graph, "A")
        self.assertNotIn("isolated", distances)

    def test_shortest_path_reconstruction(self):
        graph = build_sample_graph()
        path = shortest_path(graph, "A", "D")
        self.assertEqual(path, ["A", "C", "D"])

    def test_shortest_path_to_unreachable_node_is_none(self):
        graph = build_sample_graph()
        graph.add_node("isolated")
        self.assertIsNone(shortest_path(graph, "A", "isolated"))


if __name__ == "__main__":
    unittest.main()
