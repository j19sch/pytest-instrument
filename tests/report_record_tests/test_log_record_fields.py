import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_single_test_examples.py"
    testdir.copy_example(filename)
    return filename


def test_level_field(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    for record in records:
        assert record["level"] == "info"


def test_timestamp_field(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    for record in records:
        assert helpers.validate_timestamp(record["timestamp"], "%Y-%m-%d %H:%M:%S.%f")


def test_name_field(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    for record in records:
        assert record["name"] == "instr.report"


def test_message_field(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    assert len(records) == 3
    assert any(
        record
        for record in records
        if record["message"] == f"{tests_filename}::{test_to_run} setup passed"
    )
    assert any(
        record
        for record in records
        if record["message"] == f"{tests_filename}::{test_to_run} call passed"
    )
    assert any(
        record
        for record in records
        if record["message"] == f"{tests_filename}::{test_to_run} teardown passed"
    )


def test_filename_field(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    for record in records:
        assert record["filename"] == ""


def test_funcName_field(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    for record in records:
        assert record["funcName"] is None


def test_lineno_field(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    for record in records:
        assert record["lineno"] == 0
