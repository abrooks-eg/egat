import sys
import datetime
import os
from egautotest.loggers.test_logger import TestLogger
from egautotest.loggers.test_logger import LogLevel
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

    def startingTests(self):
        if self.log_dir:
            # Set up the log file
            start_time = datetime.datetime.now().strftime("%m-%d-%y %H.%M.%S")
            self.log_dir = self.log_dir.rstrip('/')
            self.log_dir += "/Test Run %s" % start_time
            os.mkdir(self.log_dir)
            log_name = "%s/log.txt" % self.log_dir
            self.out = open(log_name, 'w')
        else:
            self.out = sys.stdout

        # Set up the printer
        self.output_queue = Queue()
        self.printer = _Printer(self.output_queue, self.out)
        self.printer.start()
    
    def finishedTests(self):
        self.printer.tests_running = False
        self.printer.join()
        pass

    def runningTestFunction(self, classname, func, thread_num=None):
        self.current_func_failed = False
        self.current_exception = None
        self.current_traceback = None

    def finishedTestFunction(self, classname, func, thread_num=None, browser=None):
        func_str = SimpleTextLogger.format_function_name(classname, func)
        msg = ""
        if self.current_func_failed:
            msg = self.failure_msg
        else:
            msg = self.success_msg

        self.output_queue.put(
            (func_str, msg, self.current_traceback)
        )

        if self.log_level == LogLevel.DEBUG:
            self.log_debug_info(browser, classname, func)

    def skippingTestFunction(self, classname, func, thread_num=None):
        func_str = SimpleTextLogger.format_function_name(classname, func)
        self.output_queue.put((func_str, self.skipped_msg, None))

    def foundException(self, classname, func, e, tb, browser=None):
        self.current_func_failed = True
        self.current_exception = e
        self.current_traceback = tb
        if self.log_level == LogLevel.ERROR:
            self.log_debug_info(browser, classname, func)

    @staticmethod
    def format_function_name(classname, func):
        """Takes a class name and a function from that class and returns a string
        representing the given function."""
        return "%s.%s.%s" % (func.__module__, classname, func.__name__)

    def log_debug_info(self, browser, classname, func):
        """Takes a Selenium Webdriver (or None) and a classname, and function 
        object. If the browser object is not none it will take a screenshot of the 
        browser window and save the page source to the log_dir."""
        if browser:
            func_str = SimpleTextLogger.format_function_name(classname, func)
            path = self.log_dir if self.log_dir else "."
            browser.save_screenshot('%s/%s.png' % (path, func_str))
            with open('%s/%s.html' % (path, func_str), 'a') as f:
                f.write(browser.page_source.encode('utf8'))

