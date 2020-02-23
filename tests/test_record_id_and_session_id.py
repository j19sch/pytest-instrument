import pytest
from uuid import UUID

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_fixtures_and_logger_examples.py"
    testdir.copy_example(filename)
    return filename


def test_record_id(testdir, tests_filename):
    result = testdir.runpytest("-vs", "--instrument=json,log", f"{tests_filename}")
    result.assert_outcomes(error=0, failed=0, passed=4)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    for record in json_records:
        try:
            UUID(record["record_id"], version=4)
        except (AttributeError, ValueError):
            assert False, f"Record id {record['record_id']} is not a valid v4 UUID."

    record_ids = [_["record_id"] for _ in json_records]
    assert len(record_ids) == len(json_records)
    assert len(record_ids) == len(set(record_ids))

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_session_id(testdir, tests_filename):
    result = testdir.runpytest("-vs", "--instrument=json,log", f"{tests_filename}")
    result.assert_outcomes(error=0, failed=0, passed=4)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    for record in json_records:
        try:
            UUID(record["session_id"], version=4)
        except (AttributeError, ValueError):
            assert False, f"Session id {record['session_id']} is not a valid v4 UUID."

    session_ids = [_["session_id"] for _ in json_records]
    assert len(session_ids) == len(json_records)
    assert len(set(session_ids)) == 1

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)

    assert session_ids[0] in log_records[0]
