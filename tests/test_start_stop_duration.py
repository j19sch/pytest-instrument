import pytest


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_results_setup_teardown_call.py"
    testdir.copy_example(filename)
    return filename


def test_record_start(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    result.stdout.fnmatch_lines('---> record: *, "start": *')


def test_record_stop(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    result.stdout.fnmatch_lines('---> record: *, "stop": *')


def test_record_duration(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    result.stdout.fnmatch_lines('---> record: *, "duration": *')
