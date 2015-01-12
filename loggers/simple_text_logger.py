import sys
from loggers.test_logger import TestLogger

class SimpleTextLogger(TestLogger):
    """A very simple logger that writes the test method names and tracebacks in 
    plain text."""
    current_func_failed = None
    current_exception = None
    current_traceback = None

    def set_log_level(self, log_level):
        pass

    def startingTests(self):
        pass
    
    def finishedTests(self):
        pass

    def runningTestFunction(self, classname, func):
        self.current_func_failed = False
        self.current_exception = None
        self.current_traceback = None
        self.out.write("%s.%s " % (classname, func.__name__))

    def finishedTestFunction(self, classname, func):
        if self.current_func_failed:
            self.out.write("F\n%s" % self.current_traceback)
        else:
            self.out.write("S\n")

    def skippingTestFunction(self, classname, func):
        pass

    def foundException(self, classname, func, e, tb):
        self.current_func_failed = True
        self.current_exception = e
        self.current_traceback = tb
