import unittest
from egat.test_runner_helpers import WorkProvider

class MockWorkNode():
    resources = []
    i = None

class TestGetNextNode(unittest.TestCase):
    def test_empty_work_pool(self):
        wp = WorkProvider()
        self.assertIsNone(wp.get_next_node())

    def test_empty_work(self):
        wp = WorkProvider()
        self.assertEqual(None, wp.get_next_node())

    def test_single_node(self):
        wp = WorkProvider()
        node = MockWorkNode()
        wp.add_nodes(node)
        self.assertEqual(node, wp.get_next_node())

    def test_multiple_nodes(self):
        number_of_nodes = 10
        wp = WorkProvider()
        nodes = [MockWorkNode]
        for i in range(0, number_of_nodes):
            node = MockWorkNode()
            node.i = i
            nodes.append(node)
        wp.add_nodes(*nodes)

        for i in range(0, number_of_nodes):
            node = wp.get_next_node()
            self.assertEqual(node.i, nodes[i].i)

