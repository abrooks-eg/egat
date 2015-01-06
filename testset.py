import inspect

class TestSet():
    """A very general class that represents an arbitrary set of tests. By default 
    each test in a TestSet should be a instance method that begins with the string 
    'test', however the 'load_tests' method may be overridden to modify this 
    behavior. A TestSet may also include 'setup' and 'teardown' methods, called 
    before the tests in the set start and after they are finished, respectively."""

    @classmethod
    def load_tests(cls):
        """A method used by the test runner to obtain the list of test functions 
        this TestSet defines. The list returned should be a list of function 
        objects which are instance methods available to this class."""

        # Find all methods prefixed with the testMethodPrefix
        testMethodPrefix = "test"
        test_functions = []
        testFnNames = filter(lambda n,p=testMethodPrefix: 
                             n[:len(p)] == p, dir(cls))
        members = inspect.getmembers(cls, predicate=inspect.ismethod)
        for function_name, function in members:
            if function_name in testFnNames:
                test_functions.append(function)

        # Recur on superclasses to get their test methods as well
        for baseclass in cls.__bases__:
            for function in baseclass.load_tests():
                if function.__name__ not in testFnNames:  
                    testFnNames.append(testFnName)        
                    test_functions.append(function)

        return test_functions 
