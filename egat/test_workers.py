from threading import Lock
from egat.testset import ExecutionOrder
from egat.testset import TestSet
from threading import Thread
import sys
import os
import traceback
import collections
import pkgutil
import inspect

sys.path.append(os.getcwd())

class WorkManager():
    """This class manages the WorkerThreads that assist in test execution."""
    thread_count = None
    work_pools = None
    logger = None
    workers = None
    selenium_debugging_enabled = None

    def __init__(self, logger, thread_count=1, selenium_debugging=False):
        """Takes a WorkPool object, a TestLogger, and optionally the number of 
        threads that should be used to execute tests."""
        self.thread_count = thread_count
        self.work_pools = []
        self.logger = logger
        self.workers = []
        self.failed_ex_groups = set()
        self.selenium_debugging_enabled = selenium_debugging

    def add_tests(self, tests):
        """Takes a list of tests with the format: 
            {
                'test': 'test_name',
                'configuration': {
                    'var': 'val'
                },
                'environment': {
                    'var': 'val'
                }
            }
        and adds them to this WorkPool's work."""
        # Find a WorkPool that is not a user defined thread
        work_pool = None
        auto_work_pools = filter(lambda w: not w.user_defined_thread, self.work_pools)
        if auto_work_pools:
            work_pool = auto_work_pools[0]
        else:
            work_pool = self.get_new_work_pool()

        work_pool.add_tests(tests)
            
    def add_thread(self, threads, configuration={}):
        """Like add_tests except the tests passed to this function will be run in 
        their own thread. Their ResourceGroup restrictions will be ignored."""
        for thread in threads:
            work_pool = self.get_new_work_pool()
            for test in thread:
                json_test = {
                    "test": test,
                    "configuration": configuration,
                }
                work_pool.add_tests([json_test])
        

    def get_new_work_pool(self):
        """Returns a new WorkPool instance attached to this WorkManager. The WorkPool
        can have tests added to it which will be run when 'run_tests()' is called
        on this WorkManager."""
        work_pool = WorkPool(self)
        self.work_pools.append(work_pool)
        return work_pool

    def run_tests(self):
        """Instructs this WorkManager to run the tests in its WorkPools."""
        self.logger.startingTests()
        if len(self.work_pools) > 1:
            # User has defined threads, run in manual mode
            i = 0
            for work_pool in self.work_pools:
                work_pool.user_defined_threads = True
                worker = WorkerThread(self, work_pool, self.logger, thread_num=i)
                worker.start()
                self.workers.append(worker)
                i += 1

        elif len(self.work_pools) == 1:
            # We only have one big WorkPool, run in automatic mode
            for i in range(self.thread_count):
                worker = WorkerThread(self, self.work_pools[0], self.logger, thread_num=i)
                worker.start()
                self.workers.append(worker)

        for worker in self.workers:
            worker.join()
        self.logger.finishedTests()

class WorkerThread(Thread):
    """This class draws work from the WorkPool and executes it."""
    manager = None
    work_pool = None
    logger = None
    cur_node = None
    thread_num = None

    def __init__(self, manager, work_pool, logger, thread_num=None):
        """Requires a WorkManager, a WorkPool, and a TestLogger."""
        super(WorkerThread, self).__init__()
        self.manager = manager
        self.work_pool = work_pool
        self.logger = logger
        self.thread_num = thread_num

    def run(self):
        """Called when this WorkerThread is started."""
        while self.work_pool.work_nodes:
            cur_node = self.work_pool.next_available_node()

            if cur_node:
                self.run_tests_for_node(cur_node)
                # Remove this nodes resources from the thread_manager
                for resource in cur_node.resources:
                    self.work_pool.cur_resources.remove(resource)

    def run_tests_for_node(self, node):
        """Takes a WorkNode and runs the tests it contains."""
        classname = node.test_class.__name__
        # if this node contains only one function, check for failed execution groups
        # and don't instatiate the class or call setup
        if len(node.test_funcs) == 1:
            func = node.test_funcs[0]
            if self.has_failed_ex_groups(node.test_class, func):
                self.logger.skippingTestFunction(classname, func, thread_num=self.thread_num)
                return
                
        instance = node.test_class()
        setattr(instance, 'configuration', node.test_config)
        setattr(instance, 'environment', node.test_env)

        # Try to call the class's setup method
        if hasattr(instance, 'setup') and callable(instance.setup):
            instance.setup()

        # Run all the test functions
        for func in node.test_funcs:
            # Check for failed execution groups
            if self.has_failed_ex_groups(node.test_class, func):
                self.logger.skippingTestFunction(classname, func, thread_num=self.thread_num)
                continue

            # An optional Selenium Webdriver object that the logger may use to 
            # extract debugging information from.
            browser = None
            if self.manager.selenium_debugging_enabled:
                browser = getattr(instance, 'browser', None)

            self.logger.runningTestFunction(classname, func, thread_num=self.thread_num)
            try: 
                func(instance)
            except:
                e = sys.exc_info()[0]
                tb = traceback.format_exc()
                self.work_pool.add_failed_ex_groups(
                    self.get_ex_groups(func) + self.get_ex_groups(node.test_class)
                )


                self.logger.foundException(classname, func, e, tb, thread_num=self.thread_num, browser=browser)

            self.logger.finishedTestFunction(classname, func, 
                                             thread_num=self.thread_num, 
                                             browser=browser)

        # Try to call the class's teardown method
        if hasattr(instance, 'teardown') and callable(instance.teardown):
            instance.teardown()

    def has_failed_ex_groups(self, test_class, func):
        """Takes a classname and a function object in that class and checks the 
        WorkPool to see if any of the Execution Groups the function or class is a
        member of have failed. Returns True if the function is a member of a failed 
        Execution Group and False otherwise."""
        execution_groups = set(
            self.get_ex_groups(func) + self.get_ex_groups(test_class)
        )
        for ex_group in execution_groups:
            if ex_group in self.work_pool.failed_ex_groups:
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
    work_nodes = None
    next_node_id = None
    lock = None
    work_manager = None
    user_defined_threads = None
    # Execution groups that have failed. List items can be any type.
    failed_ex_groups = None 
    cur_resources = None


    def __init__(self, work_manager, user_defined_threads=False):
        self.work_nodes = []
        self.next_node_id = 1
        self.lock = Lock()
        self.work_manager = work_manager
        self.user_defined_threads = user_defined_threads
        self.failed_ex_groups = set()
        self.cur_resources = set()

    @staticmethod
    def get_classes_from_module(module_name):
        """Takes a module name like the one passed to the 'import' command and 
        returns all the classes defined in all that modules submodules."""
        classes = []
        module = __import__(module_name)
        prefix = module_name.split('.')[0] + "."
        original_modname = module_name

        for importer, module_name, ispkg in pkgutil.walk_packages(module.__path__, prefix=prefix):
            try:
                module = importer.find_module(module_name).load_module(module_name)
                mod_classes = [t[1] for t in inspect.getmembers(module, inspect.isclass)]
                classes += filter(lambda c: c.__module__.startswith(original_modname), mod_classes)
            except ImportError:
                pass

        return classes

    @staticmethod
    def is_testset(cls):
        """Takes a class object and returns True if it is a subclass of TestSet and 
        False otherwise."""
        base_classes = cls.__bases__
        for base in base_classes:
            if base == TestSet or WorkPool.is_testset(base):
                return True
        return False

    def add_tests(self, tests):
        for test in tests:
            test_name = test['test']
            configuration = test.get('configuration', {})
            environment = test.get('environment', {})

            is_module = False
            is_class = False
            is_fn = False
            try: is_module = __import__(test_name)
            except ImportError: 
                try: is_class = __import__('.'.join(test_name.split('.')[0:-1]))
                except ImportError: 
                    try: is_fn = __import__('.'.join(test_name.split('.')[0:-2]))
                    except ImportError: pass

            if is_module:
                self.add_tests_from_module(test_name, config=configuration, env=environment)
            elif is_class:
                self.add_test_class_by_name(test_name, config=configuration, env=environment)
            elif is_fn:
                self.add_test_function(test_name, config=configuration, env=environment)
            else:
                raise Exception(
                    """Expected fully-qualified module name, class name, or 
                    function, but got %s""" % (test_name)
                )

    def add_tests_from_module(self, test_name, config={}, env={}):
        """Takes a fully-qualified module name, finds all subclasses of TestSet in 
        the module and its submodules and adds their tests to this WorkPool's work."""
        classes = WorkPool.get_classes_from_module(test_name)
        classes = filter(WorkPool.is_testset, classes)
        for cls in classes:
            self.add_test_class(cls, config=config, env=env)

    def add_test_class_by_name(self, full_class_name, config={}, env={}):
        """Takes a fully-qualified class name for a TestSet subclass and adds the 
        tests in the TestSet to this WorkPool."""
        self.add_test_class(WorkPool.get_class_from_name(full_class_name), config=config, env=env)

    def add_test_function(self, full_function_name, config={}, env={}):
        """Takes a fully-qualified function name (e.g. 'module.class.function_name')
        and adds the function to this WorkPool's work."""
        class_name = '.'.join(full_function_name.split('.')[0:-1])
        function_name = full_function_name.split('.')[-1]

        test_class = WorkPool.get_class_from_name(class_name)
        func = getattr(test_class, function_name)
        self.add_node(test_class, [func], config=config, env=env)

    @staticmethod
    def get_class_from_name(full_class_name):
        """Takes a fully-qualified class name as a string and returns the class 
        object."""
        class_name = full_class_name.split('.')[-1]
        module_name = '.'.join(full_class_name.split('.')[0:-1])
        class_path = full_class_name.split('.')[1:]
        root_module = __import__(module_name)
        test_class = reduce(lambda x, y: getattr(x, y), class_path, root_module)
        return test_class

    def add_test_class(self, cls, config={}, env={}):
        """Takes a class object that should be a subclass of TestSet and adds its
        test functions to this WorkPool's work."""
        # Check to see if this is an ordered or unordered set of tests
        if cls.execution_order == ExecutionOrder.UNORDERED:
            # if it is unordered these test functions are each their own node
            for func in cls.load_tests():
                self.add_node(cls, [func], config=config, env=env)
        else:
            # if it is ordered then the test functions must all be run together
            self.add_node(cls, cls.load_tests(), config=config, env=env)

    def add_failed_ex_groups(self, failed_ex_groups):
        """Takes a list of Execution Groups and adds them to this WorkPool's list
        of failed Execution Groups."""
        for group in failed_ex_groups:
            self.failed_ex_groups.add(group)

    def add_node(self, test_class, test_funcs, config={}, env={}):
        """Takes a TestSet subclass object and a list of function objects in that 
        class and adds them as a node in the WorkPool's work. The class will be 
        instantiated and the functions called as tests."""
        new_node = WorkNode(self.next_node_id, test_class, test_funcs, config=config, env=env)
        self.next_node_id += 1
        self.work_nodes.append(new_node)

    def remove_node(self, node_to_remove):
        """Takes a WorkNode object that is in this WorkPool's work and removes it."""
        self.work_nodes.remove(node_to_remove)

    def next_available_node(self):
        """Finds and returns the next available node of work, and removes it from 
        the work pool. This method will block until work is available or the work 
        pool is empty."""
        self.lock.acquire()

        available_node = None
        for node in self.work_nodes:
            all_resources_available = True
            for resource in node.resources:
                if resource in self.cur_resources:
                    all_resources_available = False
            
            if all_resources_available:
                available_node = node
                for resource in available_node.resources:
                    self.cur_resources.add(resource)
                self.remove_node(node)
                break

        self.lock.release()

        return available_node

class WorkNode():
    """A class that represents a node in the work of a WorkPool. Each node 
    represents a unit of work (tests to be run) and defines the resources it needs 
    to share with other nodes (SharedResources). Each node has edges that connect 
    it to other nodes that share its SharedResources and thus cannot be run at the 
    same time."""
    id = None # this node's unique id
    resources = None # a list of SharedResource classes this node needs
    test_class = None # The class containing tests for this node
    test_funcs = None # The tests functions for this node
    test_config = None
    test_env = None
    user_defined_threads = None

    def __init__(self, id, test_class, test_funcs, config={}, env={}, user_defined_threads=False):
        """Takes a node id (must be unique), a TestSet subclass, and a list of test 
        methods in that TestSet subclass."""
        self.id = id
        self.resources = set()
        self.test_class = test_class
        self.test_funcs = test_funcs
        self.test_config = config
        self.test_env = env
        self.user_defined_threads = user_defined_threads

        if not user_defined_threads:
            # Add class resources
            class_resources = getattr(test_class, 'resources', [])
            self.resources = self.resources.union(set(class_resources))

            # Add function resources
            for func in test_funcs:
                for resource in getattr(func, 'resources', []):
                    self.resources.add(resource)
