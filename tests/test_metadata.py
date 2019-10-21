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

    csv_files = helpers.get_files_from_artifacts_dir_by_extension(testdir, "csv")
    assert len(csv_files) == 1

    csv_records = helpers.get_records_from_csv_file_in_artifacts_dir(
        testdir, csv_files[0]
    )

    for record in csv_records:
        try:
            UUID(record["record_id"], version=4)
        except (AttributeError, ValueError):
            assert False, f"Record id {record['record_id']} is not a valid v4 UUID."

    record_ids = [_["record_id"] for _ in csv_records]
    assert len(record_ids) == len(set(record_ids))


def test_session_id(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}", "-k in_session"
    )
    result.assert_outcomes(error=0, failed=0, passed=2)

    csv_files = helpers.get_files_from_artifacts_dir_by_extension(testdir, "csv")
    assert len(csv_files) == 1

    csv_records = helpers.get_records_from_csv_file_in_artifacts_dir(
        testdir, csv_files[0]
    )

    for record in csv_records:
        try:
            UUID(record["session_id"], version=4)
        except (AttributeError, ValueError):
            assert False, f"Session id {record['session_id']} is not a valid v4 UUID."

    session_ids = [_["session_id"] for _ in csv_records]
    assert len(set(session_ids)) == 1
