from egautotest.test_workers import WorkManager
import argparse
import json

class TestRunner():
    """ A class used to run TestSet tests."""
    tests = [] # Should be a list of tuples like [(class, [func1, func2]) ...]
    work_pool = None
    work_manager = None
    logger = None
    user_defined_threads = None

    def __init__(self, logger, number_of_threads=1, selenium_debugging=True, user_defined_threads=False):
        """Initializes the TestRunner. The logger should be a subclass of 
        TestLogger."""
        self.logger = logger
        self.user_defined_threads = user_defined_threads
        self.work_manager = WorkManager(self.logger, number_of_threads, 
                                        selenium_debugging=selenium_debugging)

    def add_tests(self, test_json):
        """Takes a JSON test object like:
            {
                'test': 'test_name',
                'configuration': {
                    'var': 'val'
                },
                'environment': {
                    'var': 'val'
                }
            }
        and adds the tests to a WorkPool."""
        if self.user_defined_threads:
            self.work_manager.add_thread(test_json['tests'], test_json.get('configuration', {})) 
        else:
            tests = TestRunner._build_tests(test_json)
            self.work_manager.add_tests(tests)

    @staticmethod
    def _build_tests(test_obj, parent_configuration={}, parent_environment={}):
        """Takes a JSON test object like the one defined in the configuration file 
        and returns a flat list of test objects in the format that add_tests 
        requires. This method takes care of building out the proper configurations 
        and environments for nested tests."""
        flat_tests = []
        # If tests is a test name
        # Base case
        if type(test_obj) in [str, unicode]:
            test = {}
            test['configuration'] = parent_configuration
            test['environment'] = parent_environment
            test['test'] = test_obj
            flat_tests.append(test)

        # current_tests is a test dict
        elif type(test_obj) is dict:
            current_configuration = test_obj.get('configuration', {})
            current_environments = test_obj.get('environments', {})
            current_tests = test_obj.get('tests', [])

            # Merge the parent configuration with the current configuration
            merged_configuration = parent_configuration.copy() 
            for key, val in current_configuration.items():
                merged_configuration[key] = val

            if current_environments:
                for current_environment in current_environments:
                    for current_test in current_tests:
                        # Merge the parent env with the current env
                        merged_environment = parent_environment.copy()
                        for key, val in current_environment.items():
                            merged_environment[key] = val

                        # Recur
                        flat_tests += TestRunner._build_tests(
                            current_test,
                            parent_configuration=merged_configuration,
                            parent_environment=merged_environment
                        )
            else:
                for subtest in current_tests:
                    flat_tests += TestRunner._build_tests(
                        subtest,
                        parent_configuration=merged_configuration,
                        parent_environment=parent_environment
                    )

        return flat_tests

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
          "-u",
          "--user-defined-threads",
          action='store_true',
          help="""A flag that signals that the user has defined which tests should
          run in which threads in the configuration file. Only valid in a 
          configuration file."""
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
         config_args.configuration = config_json.get('configuration', {})
         config_args.environments = config_json.get('environments', [])

         return config_args
      else:
         return cli_args
