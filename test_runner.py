import argparse
import sys
import traceback
import os
from loggers.simple_text_logger import SimpleTextLogger

class TestRunner():
    """ A class used to run TestSet tests."""
    tests = [] # Should be a list of tuples like [(class, [func1, func2]) ...]
    logger = None

    def __init__(self, logger):
        """Initializes the TestRunner. The logger should be a subclass of 
        TestLogger."""
        self.logger = logger

    def add_tests(self, *class_names):
        """Takes a list of fully-qualified class names and loads tests from those 
        classes. The loaded tests are added to the list of tests that this 
        TestRunner will execute. The classes should be subclasses of TestSet and 
        must implement the 'load_tests' method."""
        for full_class_name in class_names:
            if full_class_name:
                class_name = full_class_name.split('.')[-1]
                module_name = '.'.join(full_class_name.split('.')[0:-1])
                class_path = full_class_name.split('.')[1:]
                module = __import__(module_name)

                # Get the class from the module object
                for part in class_path:
                    module = getattr(module, part)

                self.tests.append((module, module.load_tests()))

    def run_tests(self):
        """Runs the tests that have been added to this TestRunner and reports the 
        results to the given TestLogger."""
        self.logger.startingTests()

        for (class_, functions) in self.tests:
            instance = class_()
            classname = class_.__name__

            # Try to call the class's setup method
            try:
                instance.setup()
            except AttributeError:
                pass # this is fine

            # Run all the test functions
            for func in functions:
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

def main():
    """The command-line interface for the TestRunner class."""

    # Define arguments
    parser = argparse.ArgumentParser(
        description="A command-line client for running functional test scripts.",
    )

    parser.add_argument(
        "-l",
        "--log",
        metavar="LOG_DIR",
        help="A path specifying the directory where the log should be written to instead of STDOUT.",
    )

    parser.add_argument(
        "-c",
        "--config",
        metavar="CONFIG_FILE",
        help="""A configuration file which can be used to specify longer lists of 
        tests. The file should contain one fully-qualified class name on each line.
        The configuration file replaces the 'class_name' command-line arguments.""",
    )

    parser.add_argument(
        "--log-level",
        metavar="LOG_LEVEL",
        choices=["DEBUG", "INFO", "ERROR"],
        default="INFO",
        help="Sets the log level. Valid values are DEBUG, INFO, ERROR. Defaults to INFO.",
    )

    parser.add_argument(
        'class_name',
        type=str,
        nargs='*',
        help="""The fully qualified class names of the scripts you wish to run. The 
        classes should be subclasses of TestSet."""
    )

    # Parse arguments
    args = parser.parse_args()
    test_classes = args.class_name
    if args.config:
        test_classes = open(args.config).read().split(os.linesep)

    # Set up the TestRunner and TestLogger
    if args.log:
        logger = SimpleTextLogger(out=open(args.log, 'a'))
    else:
        logger = SimpleTextLogger()
    logger.set_log_level(args.log_level)

    runner = TestRunner(logger)
    runner.add_tests(*test_classes) # '*' just unwraps the list

    # Run the tests
    runner.run_tests()

if __name__ == "__main__":
    main()
