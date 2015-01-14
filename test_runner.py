from egautotest.loggers.simple_text_logger import SimpleTextLogger
from egautotest.loggers.test_logger import LogLevel
from egautotest.test_runner import TestRunner
import argparse
import sys
import traceback
import os

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
    log_level = getattr(LogLevel, args.log_level)

    # Set up the TestRunner and TestLogger
    if args.log:
        logger = SimpleTextLogger(log_dir=args.log)
    else:
        logger = SimpleTextLogger()
    logger.set_log_level(log_level)

    runner = TestRunner(logger, args.number_of_threads)
    runner.add_tests(*test_classes) # '*' just unwraps the list

    # Run the tests
    runner.run_tests()

if __name__ == "__main__":
    main()
