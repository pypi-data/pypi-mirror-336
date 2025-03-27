# -*- coding: utf-8 -*-

import logging
import os
from sys import exit
from unittest import TestLoader, TextTestRunner

from click import option
from click.decorators import group
from coverage import coverage, CoverageException


@group()
def cli_tests():
    pass


@cli_tests.command("run-tests")
@option("-t", "--test-type", "test_type", default="unit")
@option("-p", "--pattern", "pattern", default="tests*.py")
def test(test_type: str, pattern: str):
    """ Runs the tests """

    if not os.path.exists(f"./tests/{test_type}"):
        print(f"The directory: {test_type} does not exist under ./tests!")
        exit(1)

    if test_type == "unit":
        # Just removing verbosity from unit tests...
        os.environ["LOGGER_LEVEL"] = str(os.getenv("LOGGER_LEVEL_FOR_TEST", logging.ERROR))

    tests = TestLoader().discover(f"./tests/{test_type}", pattern=pattern)
    result = TextTestRunner(verbosity=2).run(tests)
    if not result.wasSuccessful():
        exit(1)


@cli_tests.command("run-coverage")
@option("-s", "--save-report", "save_report", default=True)
def cov(save_report: bool = True):
    """ Runs the unit tests and generates a coverage report on success """

    os.environ["LOGGER_LEVEL"] = str(os.getenv("LOGGER_LEVEL_FOR_TEST", logging.ERROR))
    coverage_ = coverage(branch=True, source=["."])
    coverage_.start()

    tests = TestLoader().discover("./tests", pattern="tests*.py")
    result = TextTestRunner(verbosity=2).run(tests)
    coverage_.stop()

    if not result.wasSuccessful():
        exit(1)

    try:
        print("Coverage Summary:")
        coverage_.report()

        if save_report:
            coverage_.save()
            coverage_.html_report()

        coverage_.erase()

    except CoverageException as error:
        print(error)
        exit(1)
