import argparse
import json

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

      parser.add_argument(
          '--css-path',
          type=str,
          help="""An optional css file to be used with the HTMLLogger instead of the
          default one."""
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