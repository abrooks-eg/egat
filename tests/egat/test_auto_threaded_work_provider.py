import unittest
from egat.auto_threaded_test_runner import AutoThreadedWorkProvider
from collections import deque

class MockWorkNode():
    resources = []

class TestGetNextNode(unittest.TestCase):
    def test_empty_work_pool(self):
        wp = AutoThreadedWorkProvider()
        self.assertIsNone(wp.get_next_node())

    def test_no_resources(self):
        wp = AutoThreadedWorkProvider()
        node = MockWorkNode()
        wp._work_nodes = deque([node])
        self.assertEqual(node, wp.get_next_node())

    def test_single_resource(self):
        wp = AutoThreadedWorkProvider()
        node = MockWorkNode()
        wp._work_nodes = deque([node])
        node.resources = [1]
        self.assertEqual(node, wp.get_next_node())

        wp._cur_resources = [1]
        self.assertIsNone(wp.get_next_node())

    def multiple_resources(self):
        wp = AutoThreadedWorkProvider()
        node = MockWorkNode()
        wp._work_nodes = deque([node])
        node.resources = [1, 2, 3, 4]
        wp._cur_resources = [2, 3]
        self.assertIsNone(wp.get_next_node())

class TestResourcesAreFree(unittest.TestCase):
    def test_empty_required_resources(self):
        required = []
        used = [1, 2, 3, 4]
        self.assertTrue(AutoThreadedWorkProvider.resources_are_free(required, used))

    def test_empty_used_resources(self):
        required = [1, 2, 3, 4]
        used = []
        self.assertTrue(AutoThreadedWorkProvider.resources_are_free(required, used))

    def test_both_empty(self):
        required = []
        used = []
        self.assertTrue(AutoThreadedWorkProvider.resources_are_free(required, used))

    def test_neither_empty(self):
        required = [1, 2, 3, 4]
        used = [3]
        self.assertFalse(AutoThreadedWorkProvider.resources_are_free(required, used))
