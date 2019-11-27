import pytest


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_all_the_things_tests.py"
    testdir.copy_example(filename)
    return filename


def test_run_all_the_things(testdir, tests_filename):
    testdir.runpytest("-vs", "--instrument", f"{tests_filename}")
