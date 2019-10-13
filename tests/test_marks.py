import pytest


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_mark_tests.py"
    testdir.copy_example(filename)
    return filename


def test_mark_test(testdir, tests_filename):
    result = testdir.runpytest("-vs", "--instrument", f"{tests_filename}::test_mark")
    result.assert_outcomes(passed=1)

    expected_lines = [
        '---> record: *, "when": "setup", *, "marks": [[]"a_mark"[]]*',
        '---> record: *, "when": "call", *, "marks": [[]"a_mark"[]]*',
        '---> record: *, "when": "teardown", *, "marks": [[]"a_mark"[]]*',
    ]
    result.stdout.fnmatch_lines(expected_lines)


def test_multiple_mark_test(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::test_multiple_marks"
    )
    result.assert_outcomes(passed=1)

    expected_lines = [
        '---> record: *, "when": "setup", *, "marks": [[]"a_mark", "another_mark"[]]*',
        '---> record: *, "when": "call", *, "marks": [[]"a_mark", "another_mark"[]]*',
        '---> record: *, "when": "teardown", *, "marks": [[]"a_mark", "another_mark"[]]*',
    ]
    result.stdout.fnmatch_lines(expected_lines)


def test_without_mark_test(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::test_without_mark"
    )
    result.assert_outcomes(passed=1)

    expected_lines = [
        '---> record: *, "when": "setup", *, "marks": [[][]]*',
        '---> record: *, "when": "call", *, "marks": [[][]]*',
        '---> record: *, "when": "teardown", *, "marks": [[][]]*',
    ]
    result.stdout.fnmatch_lines(expected_lines)
