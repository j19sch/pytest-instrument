import pytest


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_mark_tests.py"
    testdir.copy_example(filename)
    return filename


def test_single_arg_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::test_single_arg_in_mark"
    )
    result.assert_outcomes(passed=1)

    expected_lines = [
        '---> record: *, "when": "setup", *, "labels": [[]"a_mark"[]]*',
        '---> record: *, "when": "call", *, "labels": [[]"a_mark"[]]*',
        '---> record: *, "when": "teardown", *, "labels": [[]"a_mark"[]]*',
    ]
    result.stdout.fnmatch_lines(expected_lines)


def test_single_kwarg_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::test_single_kwarg_in_mark"
    )
    result.assert_outcomes(passed=1)

    expected_lines = [
        '---> record: *, "when": "setup", *, "tags": {"my_mark": "a_mark"}*',
        '---> record: *, "when": "call", *, "tags": {"my_mark": "a_mark"}*',
        '---> record: *, "when": "teardown", *, "tags": {"my_mark": "a_mark"}*',
    ]
    result.stdout.fnmatch_lines(expected_lines)


def test_multiple_args_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::test_multiple_args_in_mark"
    )
    result.assert_outcomes(passed=1)

    expected_lines = [
        '---> record: *, "when": "setup", *, "labels": [[]"a_mark", "another_mark"[]]*',
        '---> record: *, "when": "call", *, "labels": [[]"a_mark", "another_mark"[]]*',
        '---> record: *, "when": "teardown", *, "labels": [[]"a_mark", "another_mark"[]]*',
    ]
    result.stdout.fnmatch_lines(expected_lines)


def test_multiple_kwargs_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::test_multiple_kwargs_in_mark"
    )
    result.assert_outcomes(passed=1)

    expected_lines = [
        '---> record: *, "when": "setup", *, "tags": {"my_mark": "a_mark", "my_other_mark": "another_mark"}*',
        '---> record: *, "when": "call", *, "tags": {"my_mark": "a_mark", "my_other_mark": "another_mark"}*',
        '---> record: *, "when": "teardown", *, "tags": {"my_mark": "a_mark", "my_other_mark": "another_mark"}*',
    ]
    result.stdout.fnmatch_lines(expected_lines)


def test_with_single_arg_and_single_kwarg_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::test_with_args_and_kwargs_in_mark"
    )
    result.assert_outcomes(passed=1)

    expected_lines = [
        '---> record: *, "when": "setup", *, "labels": [[]"a_mark"[]], "tags": {"my_mark": "a_mark"}*',
        '---> record: *, "when": "call", *, "labels": [[]"a_mark"[]], "tags": {"my_mark": "a_mark"}*',
        '---> record: *, "when": "teardown", *, "labels": [[]"a_mark"[]], "tags": {"my_mark": "a_mark"}*',
    ]
    result.stdout.fnmatch_lines(expected_lines)


def test_without_args_or_kwars_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::test_without_mark"
    )
    result.assert_outcomes(passed=1)

    expected_lines = [
        '---> record: *, "when": "setup", *, "labels": [[][]], "tags": {}*',
        '---> record: *, "when": "call", *, "labels": [[][]], "tags": {}*',
        '---> record: *, "when": "teardown", *, "labels": [[][]], "tags": {}*',
    ]
    result.stdout.fnmatch_lines(expected_lines)
