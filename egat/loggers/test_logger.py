from egat.test_runner_helpers import TestFunctionType


class LogLevel():
    DEBUG = 4
    INFO  = 3
    WARN  = 1 # Unused, treated the same as ERROR
    ERROR = 1

#AB - Adding a class to handle screen shot capturing levels
class LogScreen():
    ASSERT = 3
    ERROR  = 2
    NONE   = 1


class TestLogger():
    """An abstract class that defines an interface for a test logger. Intended to 
    be subclassed and have all its methods overridden."""

    log_level = None
    log_screen = None
    log_dir = None
    log_display = False

    def __init__(self, log_dir=None, log_level=LogLevel.ERROR, log_screen=LogScreen.NONE, log_display=False):
        """Takes a directory that the logger will write to and optionally a 
        LogLevel."""
        self.log_dir = log_dir
        self.log_level = log_level
        self.log_screen = log_screen
        self.log_display = log_display

    def set_log_level(self, log_level):
        """Sets the log level. Valid levels are defined in the LogLevel class."""
        self.log_level = log_level
        
    def set_log_scren(self, log_screen):
        """Sets the log level. Valid levels are defined in the LogLevel class."""
        self.log_screen = log_screen

    def set_log_display(self, log_display):
        self.log_display = log_display

    def startingTests(self):
        """Called by the test runner. Indicates that tests are starting."""
        pass
    
    def finishedTests(self):
        """Called by the test runner. Indicates that all tests are finished."""
        pass

    def runningTestFunction(self, class_instance, func, func_type=TestFunctionType.TEST, thread_num=None):
        """Called by the test runner. Indicates that the given test function from 
        the given class is about to be run."""
        pass

    def finishedTestFunction(self, class_instance, func, func_type=TestFunctionType.TEST, thread_num=None):
        """Called by the test runner. Indicates that the given test function from 
        the given class is finished running. This function should return an integer
        equal to the number of failed tests."""
        pass

    def skippingTestFunction(self, class_instance, func, func_type=TestFunctionType.TEST, thread_num=None):
        """Called by the test runner. Indicates that the given test function from
        the given class has been skipped. This method is called instead of 
        runningTestFunction()."""
        pass

    def foundException(self, class_instance, func, e, tb, func_type=TestFunctionType.TEST, thread_num=None):
        """Called by the test runner. Indicates that the given test function from 
        the given class has encountered an exception. The exception object and stack 
        trace (string) are also provided. An optional 'browser' argument may be 
        provided. The 'browser' should be a Selenium Webdriver object and may be 
        used by the logger to provide debugging information."""
        pass

    # ------------- Helper Functions --------------

    @staticmethod
    def format_function_name(instance, func):
        """Takes a class name and a function from that class and returns a string
        representing the given function."""
        return "%s.%s.%s" % (func.__module__, instance.__class__.__name__, func.__name__)

    def log_debug_info(self, instance, func):
        """Takes a class instance and a function object. If the class has an
        attribute called 'driver' this method will take a screenshot of the browser
        window and save the page source to the log_dir."""
        try:
            from selenium.webdriver.remote.webdriver import WebDriver
            #AB - change to reflect difference in front end PageModel design
            #browser = getattr(instance, 'browser', None)
            browser = None
            ss_file = None
            if hasattr(instance, 'page'):
                browser = getattr(instance.page, 'driver', None)
            
            if browser and isinstance(browser, WebDriver):
                func_str = TestLogger.format_function_name(instance, func)
                path = self.log_dir if self.log_dir else "."
                
                #Find a unique file name
                import os.path
                ss = 1
                while(os.path.isfile('%s/%s.%s.png' % (path, func_str, ss))):
                    ss += 1
                
                try:
                    browser.save_screenshot('%s/%s.%s.png' % (path, func_str, ss))
                    ss_file = '%s.%s.png' % (func_str, ss)
                    with open('%s/%s.%s.html' % (path, func_str, ss), 'w') as f:
                        f.write(browser.page_source.encode('utf8'))
                except:
                    print("error taking debugging screenshot for %s" % func_str)
                
            return ss_file 
        except ImportError:
            return None
