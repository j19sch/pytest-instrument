import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_instr_logger_examples.py"
    testdir.copy_example(filename)
    return filename


@pytest.fixture(scope="function")
def additional_module_filename(testdir):
    filename = "additional_module.py"
    testdir.copy_example(filename)
    return filename


def test_get_logger_from_request_fixture_and_emit_log_record(testdir, tests_filename):
    test_to_run = "test_logger_from_request"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    json_records_instr_log = [
        record for record in json_records if record["name"] == "instr.log"
    ]
    assert len(json_records_instr_log) == 1
    helpers.json_validate_each_record(json_records)

    record_name = "instr.log"
    record_level = "ERROR"
    record_lineno = 5
    record_message = "Oh no, there is an error!"

    result.stdout.fnmatch_lines(
        f"{record_level}    {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
    assert json_records_instr_log[0]["message"] == record_message
    assert json_records_instr_log[0]["level"] == record_level.lower()
    assert json_records_instr_log[0]["lineno"] == record_lineno
    assert json_records_instr_log[0]["name"] == record_name
    assert json_records_instr_log[0]["filename"] == tests_filename
    assert json_records_instr_log[0]["funcName"] == test_to_run

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)

    log_records_instr_log = [record for record in log_records if "instr.log" in record]
    assert len(log_records_instr_log) == len(json_records_instr_log)

    for record in log_records_instr_log:
        assert (
            f"{record_name} - {record_level} - {tests_filename}::{test_to_run} - {record_message}"
            in record
        )


def test_getLogger_and_emit_log_record(testdir, tests_filename):
    test_to_run = "test_logger_from_getLogger"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    json_records_instr_log = [
        record for record in json_records if record["name"] == "instr.log"
    ]
    assert len(json_records_instr_log) == 1
    helpers.json_validate_each_record(json_records)

    record_name = "instr.log"
    record_level = "ERROR"
    record_lineno = 9
    record_message = "Oh no, there is an error!"

    result.stdout.fnmatch_lines(
        f"{record_level}    {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
    assert json_records_instr_log[0]["message"] == record_message
    assert json_records_instr_log[0]["level"] == record_level.lower()
    assert json_records_instr_log[0]["lineno"] == record_lineno
    assert json_records_instr_log[0]["name"] == record_name
    assert json_records_instr_log[0]["filename"] == tests_filename
    assert json_records_instr_log[0]["funcName"] == test_to_run

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)

    log_records_instr_log = [record for record in log_records if "instr.log" in record]
    assert len(log_records_instr_log) == len(json_records_instr_log)

    for record in log_records_instr_log:
        assert (
            f"{record_name} - {record_level} - {tests_filename}::{test_to_run} - {record_message}"
            in record
        )


def test_sublogger_from_logger_in_request_fixture(testdir, tests_filename):
    test_to_run = "test_sub_logger_from_request"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    json_records_instr_log = [
        record for record in json_records if record["name"] == "instr.log.sublogger"
    ]
    assert len(json_records_instr_log) == 1
    helpers.json_validate_each_record(json_records)

    record_name = "instr.log.sublogger"
    record_level = "INFO"
    record_lineno = 14
    record_message = "this actually works"

    result.stdout.fnmatch_lines(
        f"{record_level}     {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
    assert json_records_instr_log[0]["message"] == record_message
    assert json_records_instr_log[0]["level"] == record_level.lower()
    assert json_records_instr_log[0]["lineno"] == record_lineno
    assert json_records_instr_log[0]["name"] == record_name
    assert json_records_instr_log[0]["filename"] == tests_filename
    assert json_records_instr_log[0]["funcName"] == test_to_run

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)

    log_records_instr_log = [record for record in log_records if "instr.log" in record]
    assert len(log_records_instr_log) == len(json_records_instr_log)

    for record in log_records_instr_log:
        assert (
            f"{record_name} - {record_level} - {tests_filename}::{test_to_run} - {record_message}"
            in record
        )


def test_sublogger_of_getLogger_logger(testdir, tests_filename):
    test_to_run = "test_sub_logger_from_getLogger"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    json_records_instr_log = [
        record for record in json_records if record["name"] == "instr.log.sublogger"
    ]
    assert len(json_records_instr_log) == 1
    helpers.json_validate_each_record(json_records)

    record_name = "instr.log.sublogger"
    record_level = "INFO"
    record_lineno = 19
    record_message = "this actually works"

    result.stdout.fnmatch_lines(
        f"{record_level}     {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
    assert json_records_instr_log[0]["message"] == record_message
    assert json_records_instr_log[0]["level"] == record_level.lower()
    assert json_records_instr_log[0]["lineno"] == record_lineno
    assert json_records_instr_log[0]["name"] == record_name
    assert json_records_instr_log[0]["filename"] == tests_filename
    assert json_records_instr_log[0]["funcName"] == test_to_run

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)

    log_records_instr_log = [record for record in log_records if "instr.log" in record]
    assert len(log_records_instr_log) == len(json_records_instr_log)

    for record in log_records_instr_log:
        assert (
            f"{record_name} - {record_level} - {tests_filename}::{test_to_run} - {record_message}"
            in record
        )


def test_logger_using_extra_kwarg(testdir, tests_filename):
    test_to_run = "test_logger_with_extra"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    json_records_instr_log = [
        record for record in json_records if record["name"] == "instr.log"
    ]
    assert len(json_records_instr_log) == 1
    helpers.json_validate_each_record(json_records)

    record_name = "instr.log"
    record_level = "INFO"
    record_lineno = 24
    record_message = "This should have something extra."

    result.stdout.fnmatch_lines(
        f"{record_level}     {record_name}:{tests_filename}:{record_lineno} {record_message}"
    )
    assert json_records_instr_log[0]["a little"] == "a lot"
    assert json_records_instr_log[0]["filename"] == tests_filename
    assert json_records_instr_log[0]["funcName"] == test_to_run
    assert json_records_instr_log[0]["lineno"] == record_lineno

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)

    log_records_instr_log = [record for record in log_records if "instr.log" in record]
    assert len(log_records_instr_log) == len(json_records_instr_log)

    for record in log_records_instr_log:
        assert (
            f"{record_name} - {record_level} - {tests_filename}::{test_to_run} - {record_message}"
            in record
        )


def test_logger_in_different_module_from_test(
    testdir, tests_filename, additional_module_filename
):
    test_to_run = "test_logger_from_different_module"
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    json_records_instr_log = [
        record for record in json_records if record["name"].startswith("instr.log")
    ]
    assert len(json_records_instr_log) == 1
    helpers.json_validate_each_record(json_records)

    record_name = f"instr.log.{additional_module_filename[:-3]}"
    record_level = "WARNING"
    record_lineno = 6
    record_message = "Warning from a different module"

    result.stdout.fnmatch_lines(
        f"{record_level}  {record_name}:{additional_module_filename}:{record_lineno} {record_message}"
    )
    assert json_records_instr_log[0]["filename"] == additional_module_filename
    assert json_records_instr_log[0]["funcName"] == "log_warning_from_child"
    assert json_records_instr_log[0]["lineno"] == record_lineno
    assert json_records_instr_log[0]["node_id"] == f"{tests_filename}::{test_to_run}"

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)

    log_records_instr_log = [record for record in log_records if "instr.log" in record]
    assert len(log_records_instr_log) == len(json_records_instr_log)

    for record in log_records_instr_log:
        assert (
            f"{record_name} - {record_level} - {tests_filename}::{test_to_run} - {record_message}"
            in record
        )
