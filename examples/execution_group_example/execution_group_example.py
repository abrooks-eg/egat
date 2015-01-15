from egautotest.execution_groups import execution_group
from egautotest.testset import SequentialTestSet

# This class demonstrates how to use an execution group. By annotating this class 
# an execution group we specify that if one of the methods in class fails then the
# rest of the methods should be skipped. Execution groups can be added to classes or
# functions, and can span multiple files as long as the id you pass to the 
# decorator stays the same. 
# You can test this by running this command from the root directory of the project:
#   python test_runner.py examples.execution_group_example.execution_group_example.TestFooCreation
@execution_group("FooExecutionGroup")
class TestFooCreation(SequentialTestSet):
    def testOpenFooPage(self):
        assert(True)

    def testClickCreateFooButton(self):
        assert(False)

    def testFooWasCreated(self):
        assert(True)
