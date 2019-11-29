import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_single_test_with_logger_examples.py"
    testdir.copy_example(filename)
    return filename


def test_file_test(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_node_id = f"{tests_filename}::{test_to_run}"
    assert len(
        [record for record in records if record["node_id"] == expected_node_id]
    ) == len(records)


def test_file_class_test(testdir, tests_filename):
    class_to_run = "TestClass"
    test_to_run = "test_in_class_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{class_to_run}::{test_to_run}"
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_node_id = f"{tests_filename}::{class_to_run}::{test_to_run}"
    assert len(
        [record for record in records if record["node_id"] == expected_node_id]
    ) == len(records)


def test_folder_file_test(testdir):
    example_folder = "subdir_example"
    tests_folder = "subdir"
    tests_filename = "test_single_test_in_subdir_examples.py"
    test_to_run = "test_passes_in_subdir"
    testdir.copy_example(example_folder)
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_folder}/{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_node_id = f"{tests_folder}/{tests_filename}::{test_to_run}"
    assert len(
        [record for record in records if record["node_id"] == expected_node_id]
    ) == len(records)
