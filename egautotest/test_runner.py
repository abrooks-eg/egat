from egautotest.test_workers import WorkManager

class TestRunner():
    """ A class used to run TestSet tests."""
    tests = [] # Should be a list of tuples like [(class, [func1, func2]) ...]
    work_pool = None
    work_manager = None
    logger = None

    def __init__(self, logger, number_of_threads=1, selenium_debugging=True):
        """Initializes the TestRunner. The logger should be a subclass of 
        TestLogger."""
        self.logger = logger
        self.work_manager = WorkManager(self.logger, number_of_threads, 
                                        selenium_debugging=selenium_debugging)

    def add_tests(self, tests):
        """Takes a list of fully-qualified class names and loads tests from those 
        classes. The loaded tests are added to the pool of tests that this 
        TestRunner will execute. The classes should be subclasses of TestSet and 
        must implement the 'load_tests' method."""
        self.work_manager.add_tests(tests)

    def run_tests(self):
        """Runs the tests that have been added to this TestRunner and reports the 
        results to the given TestLogger."""
        self.work_manager.run_tests()

