import pytest


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_results_setup_teardown_call.py"
    testdir.copy_example(filename)
    return filename


def test_result_call_passes(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest("-vs", f"{tests_filename}::{test_to_run}")
    result.assert_outcomes(error=0, failed=0, passed=1)

    result.stdout.fnmatch_lines(f'---> record: *, "when": "call", "outcome": "passed"*')


def test_result_call_fails(testdir, tests_filename):
    test_to_run = "test_fails"
    result = testdir.runpytest("-vs", f"{tests_filename}::{test_to_run}")
    result.assert_outcomes(error=0, failed=1, passed=0)

    result.stdout.fnmatch_lines(f'---> record: *, "when": "call", "outcome": "failed"*')


def test_result_setup_passes(testdir, tests_filename):
    test_to_run = "test_setup_passes"
    result = testdir.runpytest("-vs", f"{tests_filename}::{test_to_run}")
    result.assert_outcomes(error=0, failed=0, passed=1)

    result.stdout.fnmatch_lines(
        f'---> record: *, "when": "setup", "outcome": "passed"*'
    )


def test_result_setup_fails(testdir, tests_filename):
    test_to_run = "test_setup_fails"
    result = testdir.runpytest("-vs", f"{tests_filename}::{test_to_run}")
    result.assert_outcomes(error=1, failed=0, passed=0)

    result.stdout.fnmatch_lines(
        f'---> record: *, "when": "setup", "outcome": "failed"*'
    )


def test_result_teardown_passes(testdir, tests_filename):
    test_to_run = "test_teardown_passes"
    result = testdir.runpytest("-vs", f"{tests_filename}::{test_to_run}")
    result.assert_outcomes(error=0, failed=0, passed=1)

    result.stdout.fnmatch_lines(
        f'---> record: *, "when": "teardown", "outcome": "passed"*'
    )


def test_result_teardown_fails(testdir, tests_filename):
    test_to_run = "test_teardown_fails"
    result = testdir.runpytest("-vs", f"{tests_filename}::{test_to_run}")
    result.assert_outcomes(error=1, failed=0, passed=1)

    result.stdout.fnmatch_lines(
        f'---> record: *, "when": "teardown", "outcome": "failed"*'
    )


def test_result_setup_and_teardown_fail(testdir, tests_filename):
    test_to_run = "test_setup_and_teardown_fail"
    result = testdir.runpytest("-vs", f"{tests_filename}::{test_to_run}")
    result.assert_outcomes(error=1, failed=0, passed=0)

    expected_lines = [
        f'---> record: *, "when": "setup", "outcome": "failed"*',
        f'---> record: *, "when": "teardown", "outcome": "passed"*',
    ]

    result.stdout.fnmatch_lines(expected_lines)
