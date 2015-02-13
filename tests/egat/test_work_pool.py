import unittest
from egat.test_workers import WorkPool

from tests.dummy_modules.mod1 import ModuleOneHalf
from tests.dummy_modules.mod1 import ModuleTwoHalves
from tests.dummy_modules.bars.testset_subclass import TestSetSubclass
from tests.dummy_modules.bars.testset_subclass_subclass import TestSetSubclassSubclass

class MockWorkNode():
    resources = []

class TestGetClassesFromModule(unittest.TestCase):
    def test_whole_module_import(self):
        classes = WorkPool.get_classes_from_module('tests.dummy_modules')
        expected = set([
            ModuleOneHalf, 
            ModuleTwoHalves, 
            TestSetSubclass, 
            TestSetSubclassSubclass
        ])

        self.assertEqual(classes, expected)

class TestGetClassFromName(unittest.TestCase):
    def test_get_class_from_full_name(self):
        class_name = "tests.dummy_modules.mod1.ModuleOneHalf"
        cls = WorkPool.get_class_from_name(class_name)
        self.assertEqual(cls, ModuleOneHalf)

class TestIsTestSet(unittest.TestCase):
    def test_direct_subclass(self):
        self.assertTrue(WorkPool.is_testset(TestSetSubclass))

    def test_indirect_subclass(self):
        self.assertTrue(WorkPool.is_testset(TestSetSubclassSubclass))

    def test_non_testset(self):
        self.assertFalse(WorkPool.is_testset(ModuleOneHalf))
        self.assertFalse(WorkPool.is_testset(ModuleTwoHalves))

class TestNextAvailableNode(unittest.TestCase):
    def test_empty_work_pool(self):
        wp = WorkPool()
        self.assertIsNone(wp.next_available_node())

    def test_no_resources(self):
        wp = WorkPool()
        node = MockWorkNode()
        wp.work_nodes = [node]
        self.assertEqual(node, wp.next_available_node())

    def test_single_resource(self):
        wp = WorkPool()
        node = MockWorkNode()
        wp.work_nodes = [node]
        node.resources = [1]
        self.assertEqual(node, wp.next_available_node())

        wp._cur_resources = [1]
        self.assertIsNone(wp.next_available_node())

    def multiple_resources(self):
        wp = WorkPool()
        node = MockWorkNode()
        wp.work_nodes = [node]
        node.resources = [1, 2, 3, 4]
        wp._cur_resources = [2, 3]
        self.assertIsNone(wp.next_available_node())

class TestResourcesAreFree(unittest.TestCase):
    def test_empty_required_resources(self):
        required = []
        used = [1, 2, 3, 4]
        self.assertTrue(WorkPool.resources_are_free(required, used))

    def test_empty_used_resources(self):
        required = [1, 2, 3, 4]
        used = []
        self.assertTrue(WorkPool.resources_are_free(required, used))

    def test_both_empty(self):
        required = []
        used = []
        self.assertTrue(WorkPool.resources_are_free(required, used))

    def test_neither_empty(self):
        required = [1, 2, 3, 4]
        used = [3]
        self.assertFalse(WorkPool.resources_are_free(required, used))
