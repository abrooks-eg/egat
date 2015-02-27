from egat.execution_groups import execution_group
from egat.testset import SequentialTestSet

# This class demonstrates how to use an execution group. By annotating this class with
# an execution group we specify that if one of the methods in the class fails then the
# rest of the methods should be skipped. Execution groups can be added to classes or
# functions, and can span multiple files as long as the id you pass to the 
# decorator stays the same. 
# You can test this by running this command from the root directory of the project:
#   ./egatest examples.execution_group_example
#
# You should see in the test output that the testFooWasCreated() method was skipped.
@execution_group("FooExecutionGroup")
class TestFooCreation(SequentialTestSet):
    def testOpenFooPage(self):
        assert(True)

    def testClickCreateFooButton(self):
        assert(False)

    def testFooWasCreated(self):
        assert(True)
