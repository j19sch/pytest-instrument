import pytest
from uuid import UUID

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_metadata_tests.py"
    testdir.copy_example(filename)
    return filename


def test_record_id(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)
    assert len(records) == 4

    for record in records:
        try:
            UUID(record["record_id"], version=4)
        except (AttributeError, ValueError):
            assert False, f"Record id {record['record_id']} is not a valid v4 UUID."

    record_ids = [_["record_id"] for _ in records]
    assert len(record_ids) == len(records)
    assert len(record_ids) == len(set(record_ids))


def test_session_id(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}", "-k in_session"
    )
    result.assert_outcomes(error=0, failed=0, passed=2)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)
    assert len(records) == 8

    for record in records:
        try:
            UUID(record["session_id"], version=4)
        except (AttributeError, ValueError):
            assert False, f"Session id {record['session_id']} is not a valid v4 UUID."

    session_ids = [_["session_id"] for _ in records]
    assert len(session_ids) == len(records)
    assert len(set(session_ids)) == 1
