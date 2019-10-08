import pytest


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_mark_tests.py"
    testdir.copy_example(filename)
    return filename


def test_mark_test(testdir, tests_filename):
    result = testdir.runpytest("-vs", "-k", "test_mark")

    result.stdout.fnmatch_lines("---> instrument mark: ('a_mark',)*")
