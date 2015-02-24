import unittest
from egat.test_loader import TestLoader
from tests.dummy_modules.mod1 import ModuleOneHalf
from tests.dummy_modules.mod1 import ModuleTwoHalves
from tests.dummy_modules.bars.testset_subclass import TestSetSubclass
from tests.dummy_modules.bars.testset_subclass_subclass import TestSetSubclassSubclass
from egat.test_runner_helpers import WorkNode

# You can't really check two functions for equality in Python
# which means that you can't compare two WorkNodes for equality
# which means that you can't check a set of expected WorkNodes against actual WorkNodes
# which means that you can't unit test the TestLoader functions that return WorkNodes
#
# Many hours were lost to the discovery of these truths. May they RIP.

class TestGetWorkNodesForTests(unittest.TestCase):
    pass
#    def test_module(self):
#        tests = [
#            {
#                "test": "tests.dummy_modules.bars",
#                "configuration": {},
#                "environment": {},
#            }
#        ]
#
#        expected = [
#            WorkNode(TestSetSubclass, TestSetSubclass.load_tests()),
#            WorkNode(TestSetSubclassSubclass, TestSetSubclassSubclass.load_tests()),
#        ]
#        actual = TestLoader.get_work_nodes_for_tests(tests)
#
#        self.assertEqual(set(expected), set(actual))

class TestGetWorkNodesForTest(unittest.TestCase):
    pass

class TestGetWorkNodesFromModuleName(unittest.TestCase):
    pass
class TestGetWorkNodesFromClassName(unittest.TestCase):
    pass
class TestGetWorkNodesFromClass(unittest.TestCase):
    pass
class TestGetWorkNodesFromFunctionName(unittest.TestCase):
    pass
class TestGetClassNamesFromModuleName(unittest.TestCase):
    pass

class TestGetClassesFromModule(unittest.TestCase):
    def test_whole_module_import(self):
        classes = TestLoader.get_class_names_from_module('tests.dummy_modules')
        expected = set([
            "tests.dummy_modules.mod1.ModuleOneHalf",
            "tests.dummy_modules.mod1.ModuleTwoHalves",
            "tests.dummy_modules.bars.testset_subclass.TestSetSubclass",
            "tests.dummy_modules.bars.testset_subclass_subclass.TestSetSubclassSubclass",
            ])

        self.assertEqual(classes, expected)

class TestGetClassFromName(unittest.TestCase):
    def test_get_class_from_full_name(self):
        class_name = "tests.dummy_modules.mod1.ModuleOneHalf"
        cls = TestLoader.get_class_from_name(class_name)
        self.assertEqual(cls, ModuleOneHalf)
class TestIsTestSet(unittest.TestCase):
    def test_direct_subclass(self):
        self.assertTrue(TestLoader.is_testset(TestSetSubclass))
    def test_indirect_subclass(self):
        self.assertTrue(TestLoader.is_testset(TestSetSubclassSubclass))
    def test_non_testset(self):
        self.assertFalse(TestLoader.is_testset(ModuleOneHalf))
        self.assertFalse(TestLoader.is_testset(ModuleTwoHalves))

