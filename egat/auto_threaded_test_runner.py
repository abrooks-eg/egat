from egat.test_loader import TestLoader
from egat.test_runner_helpers import WorkProvider
from egat.test_runner_helpers import WorkerThread
from threading import Lock
from egat.testset import ExecutionOrder

class AutoThreadedTestRunner():
    """A class used to run TestSet tests."""
    tests = [] # Should be a list of tuples like [(class, [func1, func2]) ...]
    work_provider = None
    logger = None
    number_of_threads = None

    def __init__(self, logger, number_of_threads=1, selenium_debugging=True):
        """Initializes the AutoThreadedTestRunner. The logger should be a subclass of
        TestLogger."""
        self.number_of_threads = number_of_threads
        self.logger = logger
        self.work_provider = AutoThreadedWorkProvider()

    def add_tests(self, test_json):
        """Takes a list of tests in the format required by the configuration file 
        and adds them to the tests that this TestRunner will run."""
        tests_objs = AutoThreadedTestRunner._build_tests(test_json)
        work_nodes = TestLoader.get_work_nodes_for_tests(tests_objs)
        self.work_provider.add_nodes(*work_nodes)

    def run_tests(self):
        """Runs the tests that have been added to this AutoThreadedTestRunner."""
        self.logger.startingTests()
        workers = []

        for i in range(self.number_of_threads):
            worker = WorkerThread(self.work_provider, self.logger, thread_num=i)
            worker.start()
            workers.append(worker)

        for worker in workers:
            worker.join()
        self.logger.finishedTests()

    @staticmethod
    def _build_tests(test_obj, parent_configuration={}, parent_environment={}):
        """Takes a JSON test object like the one defined in the configuration file
        and returns a flat list of test objects in the format that add_tests
        requires. This method takes care of building out the proper configurations
        and environments for nested tests."""
        flat_tests = []
        # If tests is a test name
        # Base case
        if type(test_obj) in [str, unicode]:
            test = {}
            test['configuration'] = parent_configuration
            test['environment'] = parent_environment
            test['test'] = test_obj
            flat_tests.append(test)

        # current_tests is a test dict
        elif type(test_obj) is dict:
            current_configuration = test_obj.get('configuration', {})
            current_environments = test_obj.get('environments', {})
            current_tests = test_obj.get('tests', [])

            # Merge the parent configuration with the current configuration
            merged_configuration = parent_configuration.copy()
            for key, val in current_configuration.items():
                merged_configuration[key] = val

            if current_environments:
                for current_environment in current_environments:
                    for current_test in current_tests:
                        # Merge the parent env with the current env
                        merged_environment = parent_environment.copy()
                        for key, val in current_environment.items():
                            merged_environment[key] = val

                        # Recur
                        flat_tests += AutoThreadedTestRunner._build_tests(
                            current_test,
                            parent_configuration=merged_configuration,
                            parent_environment=merged_environment
                        )
            else:
                for subtest in current_tests:
                    flat_tests += AutoThreadedTestRunner._build_tests(
                        subtest,
                        parent_configuration=merged_configuration,
                        parent_environment=parent_environment
                    )

        return flat_tests

class AutoThreadedWorkProvider(WorkProvider):
    """A thread-safe class designed to manage WorkNodes and provide them to 
    WorkerThreads to be executed."""
    _work_nodes = None
    _lock = None
    # Execution groups that have failed. List items can be any type.
    _failed_ex_groups = None 
    _cur_resources = None


    def __init__(self):
        self._work_nodes = []
        self._lock = Lock()
        self._failed_ex_groups = set()
        self._cur_resources = set()

    def add_nodes(self, *work_nodes):
        """Takes a TestSet subclass object and a list of function objects in that 
        class and adds them as a node in the AutoThreadedWorkProvider's work. The class will be 
        instantiated and the functions called as tests."""
        self._lock.acquire()
        self._work_nodes += work_nodes
        self._lock.release()

    def get_next_node(self):
        """Finds and returns the next available node of work and returns it. When 
        the work is done the 'finished_with_node' method must be called to release 
        the node's resources. If no work is currently available, this method will 
        return."""
        self._lock.acquire()

        for node in self._work_nodes:
            if AutoThreadedWorkProvider.resources_are_free(node.resources, self._cur_resources):
                self._cur_resources = self._cur_resources.union(node.resources)
                self._work_nodes.remove(node)
                self._lock.release()
                return node

        self._lock.release()

    def finished_with_node(self, work_node):
        """Takes a work node and releases its resources. Must be called for each 
        node returned from 'get_next_node'."""
        self._lock.acquire()
        self._cur_resources = self._cur_resources.difference(work_node.resources)
        self._lock.release()

    def has_work(self):
        """Returns True if this WorkProvider still has unclaimed work, and False 
        otherwise."""
        self._lock.acquire()
        has_work = self._work_nodes
        self._lock.release()
        return has_work

    def add_failed_ex_groups(self, failed_ex_groups):
        """Takes a list of Execution Groups and adds them to this WorkProvider's list
        of failed Execution Groups. Should be called if any of this WorkProvider's tests 
        with execution groups fail."""
        self._lock.acquire()
        self._failed_ex_groups = self._failed_ex_groups.union(failed_ex_groups)
        self._lock.release()

    def has_failed_ex_groups(self, *execution_groups):
        """Takes a variable number of execution groups and returns True if any of 
        them have failed and False otherwise."""
        self._lock.acquire()
        for ex_group in execution_groups:
            if ex_group in self._failed_ex_groups:
                self._lock.release()
                return True

        self._lock.release()
        return False


    @staticmethod
    def resources_are_free(required_resources, used_resources):
        """Takes a list of required resources and returns True if none of them are 
        in the list of used_resources, and False otherwise."""
        for required_resource in required_resources:
            if required_resource in used_resources:
                return False
        return True
