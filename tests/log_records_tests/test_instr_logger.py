import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_instr_logger_examples.py"
    testdir.copy_example(filename)
    return filename


def test_emit_log_record(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    log_records = [record for record in records if record["name"] == "instr.log"]
    assert len(log_records) == 1
    helpers.json_validate_each_record(records)

    record_name = "instr.log"
    record_level = "ERROR"
    record_lineno = 5
    record_message = "Oh no, there is an error!"
    record_filename = "test_instr_logger_examples.py"
    record_funcName = "test_passes"

    result.stdout.fnmatch_lines(
        f"{record_level}    {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
    assert log_records[0]["message"] == record_message
    assert log_records[0]["level"] == record_level.lower()
    assert log_records[0]["lineno"] == record_lineno
    assert log_records[0]["name"] == record_name
    assert log_records[0]["filename"] == record_filename
    assert log_records[0]["funcName"] == record_funcName


def test_sublogger(testdir, tests_filename):
    test_to_run = "test_sub_logger"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    log_records = [
        record for record in records if record["name"] == "instr.log.sublogger"
    ]
    assert len(log_records) == 1
    helpers.json_validate_each_record(records)

    record_name = "instr.log.sublogger"
    record_level = "INFO"
    record_lineno = 12
    record_message = "this actually works"
    record_filename = "test_instr_logger_examples.py"
    record_funcName = "test_sub_logger"

    result.stdout.fnmatch_lines(
        f"{record_level}     {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
    assert log_records[0]["message"] == record_message
    assert log_records[0]["level"] == record_level.lower()
    assert log_records[0]["lineno"] == record_lineno
    assert log_records[0]["name"] == record_name
    assert log_records[0]["filename"] == record_filename
    assert log_records[0]["funcName"] == record_funcName


def test_logger_using_extra_kwarg(testdir, tests_filename):
    test_to_run = "test_logger_with_extra"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    log_records = [record for record in records if record["name"] == "instr.log"]
    assert len(log_records) == 1
    helpers.json_validate_each_record(records)

    assert log_records[0]["a little"] == "a lot"

    record_name = "instr.log"
    record_level = "INFO"
    record_lineno = 23
    record_message = "This should have something extra."

    result.stdout.fnmatch_lines(
        f"{record_level}     {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
