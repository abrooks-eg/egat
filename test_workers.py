from threading import Lock
from testset import ExecutionOrder
from threading import Thread

class WorkManager():
    """This class manages the WorkerThreads that assist in test execution."""
    thread_count = None
    work_pool = None
    logger = None
    workers = None
    cur_resources = None

    def __init__(self, work_pool, logger, thread_count=1):
        """Takes a WorkPool object, a TestLogger, and optionally the number of 
        threads that should be used to execute tests."""
        self.thread_count = thread_count
        self.work_pool = work_pool
        self.logger = logger
        self.workers = []
        self.cur_resources = set()

    def run_tests(self):
        """Instructs this WorkManager to run the tests in its WorkPool."""
        for _ in range(self.thread_count):
            worker = WorkerThread(self, self.work_pool, self.logger)
            worker.start()
            self.workers.append(worker)


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
            cur_node = None
            self.work_pool.lock.acquire()

            # TODO: The work_pool should have a method that provides an iterator 
            # for the graph or something.
            for node in self.work_pool.graph:
                all_resources_available = True
                for resource in node.resources:
                    if resource in self.manager.cur_resources:
                        all_resources_available = False
                
                if all_resources_available:
                    cur_node = node
                    for resource in cur_node.resources:
                        self.manager.cur_resources.add(resource)
                    self.work_pool.remove_node(node)
                    break

            self.work_pool.lock.release()

            if cur_node:
                self.run_test_for_node(cur_node)
                # Remove this nodes resources from the thread_manager
                for resource in cur_node.resources:
                    self.manager.cur_resources.remove(resource)


    def run_test_for_node(self, node):
        """Takes a WorkNode and runs the tests it contains."""
        self.logger.startingTests()

        instance = node.test_class()
        classname = node.test_class.__name__

        # Try to call the class's setup method
        try:
            instance.setup()
        except AttributeError:
            pass # this is fine

        # Run all the test functions
        for func in node.test_funcs:
            self.logger.runningTestFunction(classname, func)

            try: 
                func(instance)
            except:
                e = sys.exc_info()[0]
                tb = traceback.format_exc()
                self.logger.foundException(classname, func, e, tb)

            self.logger.finishedTestFunction(classname, func)

        # Try to call the class's teardown method
        try:
            instance.teardown()
        except AttributeError:
            pass # this is fine

        self.logger.finishedTests()

class WorkPool():
    """A class designed to hold a number of tests and their dependencies."""
    graph = None
    next_node_id = None
    lock = None

    def __init__(self):
        self.graph = []
        self.next_node_id = 1
        self.lock = Lock()

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
