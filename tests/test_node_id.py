import pytest


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_suite_structures.py"
    testdir.copy_example(filename)
    return filename


def test_file_test(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest("-vs", "-k", test_to_run)

    result.stdout.fnmatch_lines(f"---> result: {tests_filename}::{test_to_run}*")


def test_file_class_test(testdir, tests_filename):
    class_to_run = "TestClass"
    test_to_run = "test_passes"
    result = testdir.runpytest("-vs", "-k", class_to_run)

    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::{class_to_run}::{test_to_run}*"
    )


def test_folder_file_test(testdir):
    tests_folder = "subdir"
    tests_filename = "test_suite_structures_subdir.py"
    test_to_run = "test_passes_in_subdir"
    testdir.copy_example(".")
    result = testdir.runpytest("-vs", "-k", test_to_run)

    result.stdout.fnmatch_lines(
        f"---> result: {tests_folder}/{tests_filename}::{test_to_run}*"
    )
