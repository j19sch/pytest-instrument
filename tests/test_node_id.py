import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_fixtures_and_logger_examples.py"
    testdir.copy_example(filename)
    return filename


def test_with_test_as_function(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_node_id = f"{tests_filename}::{test_to_run}"
    assert len(
        [record for record in json_records if record["node_id"] == expected_node_id]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert all(expected_node_id in record for record in log_records[1:])
    assert len(log_records[1:]) == len(json_records)


def test_with_test_in_class(testdir, tests_filename):
    class_to_run = "TestClass"
    test_to_run = "test_in_class_passes"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        f"{tests_filename}::{class_to_run}::{test_to_run}",
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_node_id = f"{tests_filename}::{class_to_run}::{test_to_run}"
    assert len(
        [record for record in json_records if record["node_id"] == expected_node_id]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert all(expected_node_id in record for record in log_records[1:])
    assert len(log_records[1:]) == len(json_records)


def test_with_test_in_folder(testdir):
    example_folder = "subdir_example"
    tests_folder = "subdir"
    tests_filename = "test_single_test_in_subdir_examples.py"
    test_to_run = "test_with_logger_passes_in_subdir"
    testdir.copy_example(example_folder)
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        f"{tests_folder}/{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_node_id = f"{tests_folder}/{tests_filename}::{test_to_run}"
    assert len(
        [record for record in json_records if record["node_id"] == expected_node_id]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert all(expected_node_id in record for record in log_records[1:])
    assert len(log_records[1:]) == len(json_records)


def test_with_test_using_all_fixtures_and_loggers(testdir, tests_filename):
    test_to_run = "test_with_all_fixtures_and_logger"
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_node_id = f"{tests_filename}::{test_to_run}"
    assert len(
        [record for record in json_records if record["node_id"] == expected_node_id]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert all(expected_node_id in record for record in log_records[1:])
    assert len(log_records[1:]) == len(json_records)
