from threading import Lock
from testset import ExecutionOrder
from threading import Thread
import sys
import traceback

class WorkManager():
    """This class manages the WorkerThreads that assist in test execution."""
    thread_count = None
    work_pool = None
    logger = None
    workers = None
    selenium_debugging_enabled = None
    cur_resources = None
    # Execution groups that have failed. List items can be any type.
    failed_ex_groups = None 

    def __init__(self, logger, thread_count=1, selenium_debugging=False):
        """Takes a WorkPool object, a TestLogger, and optionally the number of 
        threads that should be used to execute tests."""
        self.thread_count = thread_count
        self.work_pool = WorkPool(self)
        self.logger = logger
        self.workers = []
        self.cur_resources = set()
        self.failed_ex_groups = set()
        self.selenium_debugging_enabled = selenium_debugging

    def add_test_class_by_name(self, full_class_name):
        """Takes a fully-qualified class name for a TestSet subclass and adds the 
        tests in the TestSet to the WorkPool."""
        self.work_pool.add_test_class_by_name(full_class_name)

    def run_tests(self):
        """Instructs this WorkManager to run the tests in its WorkPool."""
        self.logger.startingTests()
        for _ in range(self.thread_count):
            worker = WorkerThread(self, self.work_pool, self.logger)
            worker.start()
            self.workers.append(worker)

        for worker in self.workers:
            worker.join()
        self.logger.finishedTests()

    def add_failed_ex_groups(self, failed_ex_groups):
        """Takes a list of Execution Groups and adds them to the WorkManager's list
        of failed Execution Groups."""
        for group in failed_ex_groups:
            self.failed_ex_groups.add(group)

class WorkerThread(Thread):
    """This class draws work from the WorkPool and executes it."""
    manager = None
    work_pool = None
    logger = None
    cur_node = None

    def __init__(self, manager, work_pool, logger):
        """Requires a WorkManager, a WorkPool, and a TestLogger."""
        super(WorkerThread, self).__init__()
        self.manager = manager
        self.work_pool = work_pool
        self.logger = logger

    def run(self):
        """Called when this WorkerThread is started."""
        while self.work_pool.graph:
            cur_node = self.work_pool.next_available_node()

            if cur_node:
                self.run_tests_for_node(cur_node)
                # Remove this nodes resources from the thread_manager
                for resource in cur_node.resources:
                    self.manager.cur_resources.remove(resource)

    def run_tests_for_node(self, node):
        """Takes a WorkNode and runs the tests it contains."""
        classname = node.test_class.__name__
        # if this node contains only one function, check for failed execution groups
        # and don't instatiate the class or call setup
        if len(node.test_funcs) == 1:
            func = node.test_funcs[0]
            if self.has_failed_ex_groups(node.test_class, func):
                self.logger.skippingTestFunction(classname, func)
                return
                
        instance = node.test_class()

        # Try to call the class's setup method
        if hasattr(instance, 'setup') and callable(instance.setup):
            instance.setup()

        # Run all the test functions
        for func in node.test_funcs:
            # Check for failed execution groups
            if self.has_failed_ex_groups(node.test_class, func):
                self.logger.skippingTestFunction(classname, func)
                continue

            # An optional Selenium Webdriver object that the logger may use to 
            # extract debugging information from.
            browser = None
            if self.manager.selenium_debugging_enabled:
                browser = getattr(instance, 'browser', None)

            self.logger.runningTestFunction(classname, func)
            try: 
                func(instance)
            except:
                e = sys.exc_info()[0]
                tb = traceback.format_exc()
                self.manager.add_failed_ex_groups(
                    self.get_ex_groups(func) + self.get_ex_groups(node.test_class)
                )


                self.logger.foundException(classname, func, e, tb, browser=browser)

            self.logger.finishedTestFunction(classname, func, browser=browser)

        # Try to call the class's teardown method
        if hasattr(instance, 'teardown') and callable(instance.teardown):
            instance.teardown()

    def has_failed_ex_groups(self, test_class, func):
        """Takes a classname and a function object in that class and checks the 
        WorkManager to see if any of the Execution Groups the function or class is a
        member of have failed. Returns True if the function is a member of a failed 
        Execution Group and False otherwise."""
        execution_groups = set(
            self.get_ex_groups(func) + self.get_ex_groups(test_class)
        )
        for ex_group in execution_groups:
            if ex_group in self.manager.failed_ex_groups:
                return True

        return False

    def get_ex_groups(self, func_or_class):
        """Takes an object and safely tries to get its Execution Groups. Returns 
        either a list of Execution Groups or an empty list."""
        if hasattr(func_or_class, 'execution_groups'):
            return func_or_class.execution_groups
        else:
            return []


class WorkPool():
    """A class designed to hold a number of tests and their dependencies."""
    graph = None
    next_node_id = None
    lock = None
    work_manager = None

    def __init__(self, work_manager):
        self.graph = []
        self.next_node_id = 1
        self.lock = Lock()
        self.work_manager = work_manager

    def add_test_class_by_name(self, full_class_name):
        """Takes a fully-qualified class name for a TestSet subclass and adds the 
        tests in the TestSet to this WorkPool."""
        class_name = full_class_name.split('.')[-1]
        module_name = '.'.join(full_class_name.split('.')[0:-1])
        class_path = full_class_name.split('.')[1:]
        test_module = __import__(module_name)

        # Get the class from the module object
        for part in class_path:
            test_module = getattr(test_module, part)

        # Check to see if this is an ordered or unordered set of tests
        if test_module.execution_order == ExecutionOrder.UNORDERED:
            # if it is unordered these test functions are each their own node
            for func in test_module.load_tests():
                self.add_node(test_module, [func])
        else:
            # if it is ordered then the test functions must all be run together
            self.add_node(test_module, test_module.load_tests())

    def add_node(self, test_class, test_funcs):
        """Takes a TestSet subclass object and a list of function objects in that 
        class and adds them as a node in the WorkPool's graph. The class will be 
        instantiated and the functions called as tests."""
        new_node = WorkNode(self.next_node_id, test_class, test_funcs)
        self.next_node_id += 1

        # Look for conflicts with this class's SharedResources
        # Conflicts are encoded as edges in the graph
        for node in self.graph:
            for resource in new_node.resources:
                if resource in node.resources:
                    # Add an edge
                    node.edges.add(new_node.id)
                    new_node.edges.add(node.id)

        self.graph.append(new_node)

    def remove_node(self, node_to_remove):
        """Takes a WorkNode object that is in this WorkPool's graph and removes it 
        from the graph."""
        self.graph.remove(node_to_remove)
        for target_node_id in node_to_remove.edges:
            for node in self.graph:
                if node.id == target_node_id:
                    node.edges.remove(node_to_remove.id)

    def next_available_node(self):
        """Finds and returns the next available node of work, and removes it from 
        the graph. This method will block until work is available or the graph is
        empty."""
        self.lock.acquire()

        available_node = None
        for node in self.graph:
            all_resources_available = True
            for resource in node.resources:
                if resource in self.work_manager.cur_resources:
                    all_resources_available = False
            
            if all_resources_available:
                available_node = node
                for resource in available_node.resources:
                    self.work_manager.cur_resources.add(resource)
                self.remove_node(node)
                break

        self.lock.release()

        return available_node

class WorkNode():
    """A class that represents a node in the graph of a WorkPool. Each node 
    represents a unit of work (tests to be run) and defines the resources it needs 
    to share with other nodes (SharedResources). Each node has edges that connect 
    it to other nodes that share its SharedResources and thus cannot be run at the 
    same time."""
    id = None # this node's unique id
    edges = None # a list of other node ids that this node shares an edge with
    resources = None # a list of SharedResource classes this node needs
    test_class = None # The class containing tests for this node
    test_funcs = None # The tests functions for this node

    def __init__(self, id, test_class, test_funcs):
        """Takes a node id (must be unique), a TestSet subclass, and a list of test 
        methods in that TestSet subclass."""
        self.id = id
        self.edges = set()
        self.resources = set()
        self.test_class = test_class
        self.test_funcs = test_funcs

        # Add class resources
        class_resources = getattr(test_class, 'resources', [])
        self.resources = self.resources.union(set(class_resources))

        # Add function resources
        for func in test_funcs:
            for resource in getattr(func, 'resources', []):
                self.resources.add(resource)
