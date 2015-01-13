import sys
from loggers.test_logger import TestLogger
from loggers.test_logger import LogLevel
from Queue import Queue
from Queue import Empty
from threading import Thread

class _Printer(Thread):
    """A class used by the SimpleTextLogger to print test output. The _Printer reads
    from a synchronized queue so that output from tests running in multiple threads
    does not overlap."""
    tests_running = False

    def __init__(self, output_queue, out):
        super(_Printer, self).__init__()
        self.output_queue = output_queue
        self.out = out
        self.tests_running = True

    def run(self):
        while True:
            try:
                (func_str, msg, traceback) = self.output_queue.get_nowait()
                if traceback:
                    self.out.write("%s %s\n%s" % (func_str, msg, traceback))
                else:
                    self.out.write("%s %s\n" % (func_str, msg))
            except Empty:
                if not self.tests_running:
                    break

class SimpleTextLogger(TestLogger):
    """A very simple logger that writes the test method names and tracebacks in 
    plain text."""
    current_func_failed = None
    current_exception = None
    current_traceback = None
    failure_msg = "Failure"
    success_msg = "Success"
    skipped_msg = "Skipped"
    output_queue = None

    def __init__(self, out=sys.stdout, log_level=LogLevel.ERROR):
        TestLogger.__init__(self, out, log_level)
        self.output_queue = Queue()
        self.printer = _Printer(self.output_queue, self.out)
        self.printer.start()

    def set_log_level(self, log_level):
        pass

    def startingTests(self):
        pass
    
    def finishedTests(self):
        self.printer.tests_running = False
        self.printer.join()
        pass

    def runningTestFunction(self, classname, func):
        self.current_func_failed = False
        self.current_exception = None
        self.current_traceback = None

    def finishedTestFunction(self, classname, func):
        func_str = SimpleTextLogger.format_function_name(classname, func)
        msg = ""
        if self.current_func_failed:
            msg = self.failure_msg
        else:
            msg = self.success_msg

        self.output_queue.put(
            (func_str, msg, self.current_traceback)
        )

    def skippingTestFunction(self, classname, func):
        func_str = SimpleTextLogger.format_function_name(classname, func)
        self.output_queue.put((func_str, self.skipped_msg, None))

    def foundException(self, classname, func, e, tb):
        self.current_func_failed = True
        self.current_exception = e
        self.current_traceback = tb

    @staticmethod
    def format_function_name(classname, func):
        """Takes a class name and a function from that class and returns a string
        representing the given function."""
        return "%s.%s " % (classname, func.__name__)
