#!python
from egautotest.loggers.simple_text_logger import SimpleTextLogger
from egautotest.loggers.test_logger import LogLevel
from egautotest.test_runner import TestRunner
from egautotest.test_runner import ArgumentParser

def main():
    """The command-line interface for the TestRunner class."""
    # Parse arguments
    parser = ArgumentParser()
    args = parser.parse_args()
    tests = args.tests
    log_level = args.log_level

    # Set up the TestRunner and TestLogger
    if args.log:
        logger = SimpleTextLogger(log_dir=args.log)
    else:
        logger = SimpleTextLogger()
    logger.set_log_level(log_level)

    runner = TestRunner(logger, args.number_of_threads)
    runner.add_tests(tests) 

    # Run the tests
    runner.run_tests()

if __name__ == "__main__":
    main()
