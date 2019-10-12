import pytest


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_mark_tests.py"
    testdir.copy_example(filename)
    return filename


def test_mark_test(testdir, tests_filename):
    result = testdir.runpytest("-vs", f"{tests_filename}::test_mark")
    result.assert_outcomes(passed=1)

    result.stdout.fnmatch_lines("---> marks: ('a_mark',)")


def test_multiple_mark_test(testdir, tests_filename):
    result = testdir.runpytest("-vs", f"{tests_filename}::test_multiple_marks")
    result.assert_outcomes(passed=1)

    result.stdout.fnmatch_lines("---> marks: ('a_mark', 'another_mark')")


def test_without_mark_test(testdir, tests_filename):
    result = testdir.runpytest("-vs", f"{tests_filename}::test_without_mark")
    result.assert_outcomes(passed=1)

    result.stdout.fnmatch_lines("---> marks: ()")
