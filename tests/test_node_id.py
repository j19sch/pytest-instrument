import pytest


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_suite_structures.py"
    testdir.copy_example(filename)
    return filename


def test_file_test(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest("-vs", f"{tests_filename}::{test_to_run}")
    result.assert_outcomes(passed=1)

    expected_lines = [
        f'---> record: *"node_id": "{tests_filename}::{test_to_run}", "when": "setup", *',
        f'---> record: *"node_id": "{tests_filename}::{test_to_run}", "when": "call", *',
        f'---> record: *"node_id": "{tests_filename}::{test_to_run}", "when": "teardown", *',
    ]
    result.stdout.fnmatch_lines(expected_lines)


def test_file_class_test(testdir, tests_filename):
    class_to_run = "TestClass"
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", f"{tests_filename}::{class_to_run}::{test_to_run}"
    )
    result.assert_outcomes(passed=1)

    expected_lines = [
        f'---> record: *"node_id": "{tests_filename}::{class_to_run}::{test_to_run}", "when": "setup", *',
        f'---> record: *"node_id": "{tests_filename}::{class_to_run}::{test_to_run}", "when": "call", *',
        f'---> record: *"node_id": "{tests_filename}::{class_to_run}::{test_to_run}", "when": "teardown", *',
    ]
    result.stdout.fnmatch_lines(expected_lines)


def test_folder_file_test(testdir):
    tests_folder = "subdir"
    tests_filename = "test_suite_structures_subdir.py"
    test_to_run = "test_passes_in_subdir"
    testdir.copy_example(".")
    result = testdir.runpytest("-vs", f"{tests_folder}/{tests_filename}::{test_to_run}")
    result.assert_outcomes(passed=1)

    expected_lines = [
        f'---> record: *"node_id": "{tests_folder}/{tests_filename}::{test_to_run}", "when": "setup", *',
        f'---> record: *"node_id": "{tests_folder}/{tests_filename}::{test_to_run}", "when": "call", *',
        f'---> record: *"node_id": "{tests_folder}/{tests_filename}::{test_to_run}", "when": "teardown", *',
    ]
    result.stdout.fnmatch_lines(expected_lines)
