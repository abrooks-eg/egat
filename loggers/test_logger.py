import sys

class TestLogger():
    """An abstract class that defines an interface for a test logger. Intended to 
    be subclassed and have all its methods overridden."""

    out = None

    def __init__(self, out=sys.stdout):
        """Takes a stream that the logger will write to."""
        self.out = out

    def set_log_level(self, log_level):
        """Sets the log level. Valid levels are DEBUG, INFO, and ERROR."""
        pass

    def startingTests(self):
        """Called by the test runner. Indicates that tests are starting."""
        pass
    
    def finishedTests(self):
        """Called by the test runner. Indicates that all tests are finished."""
        pass

    def runningTestFunction(self, classname, func):
        """Called by the test runner. Indicates that the given test function from 
        the given class is about to be run."""
        pass

    def finishedTestFunction(self, classname, func):
        """Called by the test runner. Indicates that the given test function from 
        the given class is finished running."""
        pass

    def foundException(self, classname, func, e, tb):
        """Called by the test runner. Indicates that the given test function from 
        the given class has encountered an exception. The exception object and stack 
        trace (string) are also provided."""
        pass
