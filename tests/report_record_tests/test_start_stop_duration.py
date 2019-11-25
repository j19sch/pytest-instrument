import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_results_setup_teardown_call.py"
    testdir.copy_example(filename)
    return filename


def test_record_start(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    for record in records:
        assert float(record["start"]).is_integer() is False


def test_record_stop(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    for record in records:
        assert float(record["stop"]).is_integer() is False


def test_record_duration(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    for record in records:
        assert float(record["duration"]).is_integer() is False
