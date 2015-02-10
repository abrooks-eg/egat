import sys

class LogLevel():
    DEBUG = 4
    INFO  = 1 # Unused, treated the same as ERROR
    WARN  = 1 # Unused, treated the same as ERROR
    ERROR = 1


class TestLogger():
    """An abstract class that defines an interface for a test logger. Intended to 
    be subclassed and have all its methods overridden."""

    log_level = None
    log_dir = None

    def __init__(self, log_dir=None, log_level=LogLevel.ERROR):
        """Takes a directory that the logger will write to and optionally a 
        LogLevel."""
        self.log_dir = log_dir
        self.log_level = log_level

    def set_log_level(self, log_level):
        """Sets the log level. Valid levels are defined in the LogLevel class."""
        self.log_level = log_level

    def startingTests(self):
        """Called by the test runner. Indicates that tests are starting."""
        pass
    
    def finishedTests(self):
        """Called by the test runner. Indicates that all tests are finished."""
        pass

    def runningTestFunction(self, classname, func, thread_num=None):
        """Called by the test runner. Indicates that the given test function from 
        the given class is about to be run."""
        pass

    def finishedTestFunction(self, classname, func, thread_num=None, browser=None):
        """Called by the test runner. Indicates that the given test function from 
        the given class is finished running."""
        pass

    def skippingTestFunction(self, classname, func, thread_num=None):
        """Called by the test runner. Indicates that the given test function from
        the given class has been skipped. This method is called instead of 
        runningTestFunction()."""
        pass

    def foundException(self, classname, func, e, tb, thread_num=None, browser=None):
        """Called by the test runner. Indicates that the given test function from 
        the given class has encountered an exception. The exception object and stack 
        trace (string) are also provided. An optional 'browser' argument may be 
        provided. The 'browser' should be a Selenium Webdriver object and may be 
        used by the logger to provide debugging information."""
        pass
