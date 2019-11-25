import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_instr_logger_tests.py"
    testdir.copy_example(filename)
    return filename


def test_emit_log_record(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs",
        "--instrument",
        "--log-cli-level=debug",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)
