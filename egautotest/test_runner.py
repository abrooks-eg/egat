from egautotest.test_workers import WorkManager
import argparse

class TestRunner():
    """ A class used to run TestSet tests."""
    tests = [] # Should be a list of tuples like [(class, [func1, func2]) ...]
    work_pool = None
    work_manager = None
    logger = None

    def __init__(self, logger, number_of_threads=1, selenium_debugging=True):
        """Initializes the TestRunner. The logger should be a subclass of 
        TestLogger."""
        self.logger = logger
        self.work_manager = WorkManager(self.logger, number_of_threads, 
                                        selenium_debugging=selenium_debugging)

    def add_tests(self, tests):
        """Takes a list of fully-qualified class names and loads tests from those 
        classes. The loaded tests are added to the pool of tests that this 
        TestRunner will execute. The classes should be subclasses of TestSet and 
        must implement the 'load_tests' method."""
        self.work_manager.add_tests(tests)

    def run_tests(self):
        """Runs the tests that have been added to this TestRunner and reports the 
        results to the given TestLogger."""
        self.work_manager.run_tests()

class ArgumentParser():
   """A custom argument parser used to parse the command-line arguments or 
   configuration file for the TestRunner. This ArgumentParser uses an interface
   similar to argparse.ArgumentParser but is not a strict subclass of it."""

   def __init__(self):
      # Define arguments
      parser = argparse.ArgumentParser(
         description="A command-line client for running functional test scripts.",
      )
      self.parser = parser

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
         If this flag is present all other flags on the command line will be ignored.""",
      )

      parser.add_argument(
         "-t",
         "--number-of-threads",
         metavar="NUMBER_OF_THREADS",
         type=int,
         default=1,
         help="""An integer specifying the number of threads the tests should be run
         in. Defaults to 1.""",
      )

      parser.add_argument(
         "--log-level",
         metavar="LOG_LEVEL",
         choices=["DEBUG", "ERROR"],
         default="ERROR",
         help="Sets the log level. Valid values are DEBUG, ERROR. Defaults to ERROR.",
      )

      parser.add_argument(
         'tests',
         type=str,
         nargs='*',
         help="""The fully qualified module, class, or function names of the scripts 
         you wish to run. Classes should be subclasses of TestSet."""
      )



   def parse_args(self):
      """Parses the command-line arguments to this script, and parse the given 
      configuration file (if any).  Returns a Namespace containing the resulting 
      options. This method will use the configuration file parameters if any exist, 
      otherwise it will use the command-line arguments."""
      # Parse sys.argv
      cli_args = self.parser.parse_args()

      if cli_args.config:
         # Parse the configuration file
         config_file = open(cli_args.config, 'r')
         config_json = json.load(config_file)
         config_opts = config_json.get('options', {})

         # Turn JSON options into a flat list of strings for the parser
         args = reduce(lambda l, t: l + [str(t[0]), str(t[1])], config_opts.items(), [])
         args = filter(lambda x: x is not None, args)

         # Pass the configuration file options to the parser
         config_args = self.parser.parse_args(args=args)
         config_args.tests = config_json.get('tests', [])

         return config_args
      else:
         return cli_args
