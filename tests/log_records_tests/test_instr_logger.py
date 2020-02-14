import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_instr_logger_examples.py"
    testdir.copy_example(filename)
    return filename


def test_get_logger_from_request_fixture_and_emit_log_record(testdir, tests_filename):
    test_to_run = "test_logger_from_request"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    log_records = [record for record in records if record["name"] == "instr.log"]
    assert len(log_records) == 1
    helpers.json_validate_each_record(records)

    record_name = "instr.log"
    record_level = "ERROR"
    record_lineno = 5
    record_message = "Oh no, there is an error!"

    result.stdout.fnmatch_lines(
        f"{record_level}    {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
    assert log_records[0]["message"] == record_message
    assert log_records[0]["level"] == record_level.lower()
    assert log_records[0]["lineno"] == record_lineno
    assert log_records[0]["name"] == record_name
    assert log_records[0]["filename"] == tests_filename
    assert log_records[0]["funcName"] == test_to_run


def test_getLogger_and_emit_log_record(testdir, tests_filename):
    test_to_run = "test_logger_from_getLogger"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    log_records = [record for record in records if record["name"] == "instr.log"]
    assert len(log_records) == 1
    helpers.json_validate_each_record(records)

    record_name = "instr.log"
    record_level = "ERROR"
    record_lineno = 9
    record_message = "Oh no, there is an error!"

    result.stdout.fnmatch_lines(
        f"{record_level}    {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
    assert log_records[0]["message"] == record_message
    assert log_records[0]["level"] == record_level.lower()
    assert log_records[0]["lineno"] == record_lineno
    assert log_records[0]["name"] == record_name
    assert log_records[0]["filename"] == tests_filename
    assert log_records[0]["funcName"] == test_to_run


def test_sublogger_from_logger_in_request_fixture(testdir, tests_filename):
    test_to_run = "test_sub_logger_from_request"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    log_records = [
        record for record in records if record["name"] == "instr.log.sublogger"
    ]
    assert len(log_records) == 1
    helpers.json_validate_each_record(records)

    record_name = "instr.log.sublogger"
    record_level = "INFO"
    record_lineno = 14
    record_message = "this actually works"

    result.stdout.fnmatch_lines(
        f"{record_level}     {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
    assert log_records[0]["message"] == record_message
    assert log_records[0]["level"] == record_level.lower()
    assert log_records[0]["lineno"] == record_lineno
    assert log_records[0]["name"] == record_name
    assert log_records[0]["filename"] == tests_filename
    assert log_records[0]["funcName"] == test_to_run


def test_sublogger_of_getLogger_logger(testdir, tests_filename):
    test_to_run = "test_sub_logger_from_getLogger"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    log_records = [
        record for record in records if record["name"] == "instr.log.sublogger"
    ]
    assert len(log_records) == 1
    helpers.json_validate_each_record(records)

    record_name = "instr.log.sublogger"
    record_level = "INFO"
    record_lineno = 19
    record_message = "this actually works"

    result.stdout.fnmatch_lines(
        f"{record_level}     {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
    assert log_records[0]["message"] == record_message
    assert log_records[0]["level"] == record_level.lower()
    assert log_records[0]["lineno"] == record_lineno
    assert log_records[0]["name"] == record_name
    assert log_records[0]["filename"] == tests_filename
    assert log_records[0]["funcName"] == test_to_run


def test_logger_using_extra_kwarg(testdir, tests_filename):
    test_to_run = "test_logger_with_extra"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    log_records = [record for record in records if record["name"] == "instr.log"]
    assert len(log_records) == 1
    helpers.json_validate_each_record(records)

    record_name = "instr.log"
    record_level = "INFO"
    record_lineno = 24
    record_message = "This should have something extra."

    result.stdout.fnmatch_lines(
        f"{record_level}     {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
    assert log_records[0]["a little"] == "a lot"
    assert log_records[0]["filename"] == tests_filename
    assert log_records[0]["funcName"] == test_to_run
    assert log_records[0]["lineno"] == record_lineno
