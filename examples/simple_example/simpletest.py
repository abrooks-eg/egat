from egat.testset import SequentialTestSet
from egat.testset import UnorderedTestSet

# This is a very basic test class. It subclasses SequentialTestSet, which is a 
# subclass of TestSet. SequentialTestSet runs all the instance methods in its class 
# that start with the prefix 'test' and it runs them in the order they are defined.
#
# You can run this example from the root directory of this project by running:
#   python test_runner.py examples.simple_example.simpletest.SimpleSequentialTests
class SimpleSequentialTests(SequentialTestSet):

    # This is a simple test method. The TestRunner knows it is a test method because
    # the method name starts with the word 'test'. 
    def test1(self):
        assert(True)

    # This test makes use of a non-test method in SimpleSequentialTests
    def test2(self):
        number = 1
        assert(number == self.non_test_method(number))

    # This test should fail
    def test3(self):
        assert(False)

    # This is a non-test method. It will not be run by the test runner because its 
    # name does not start with the word 'test'
    def non_test_method(self, number):
        return number
        
# This test class subclasses UnorderedTestSet. Subclasses of UnorderedTestSet have 
# their test methods run in an undefined order. This means that the tests should be 
# independent of each other like unit tests. 
#
# You can run this class with the command:
#   python test_runner.py examples.simple_example.simpletest.SimpleUnorderedTests
class SimpleUnorderedTests(UnorderedTestSet):
    def test1(self):
        assert(True)

    def test2(self):
        assert(True)

    def test3(self):
        assert(True)
