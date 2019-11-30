from pathlib import PurePath
from uuid import UUID

import pytest

from tests import helpers
from tests.helpers import validate_timestamp


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_single_test_examples.py"
    testdir.copy_example(filename)
    return filename


def test_single_log_file_is_created_with_instrument_option(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    log_files = helpers.get_files_from_artifacts_dir_by_extension(testdir, "log")
    assert len(log_files) == 1

    split_log_file_basename = PurePath(log_files[0]).stem.split("_", maxsplit=1)
    validate_timestamp(split_log_file_basename[0], "%Y%m%dT%H%M%S")
    try:
        UUID(split_log_file_basename[1], version=4)
    except (AttributeError, ValueError):
        assert (
            False
        ), f"Log file name uuid {split_log_file_basename[1]} is not a valid v4 UUID."


def test_no_file_created_without_instrument_option(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest("-vs", f"{tests_filename}::{test_to_run}")
    result.assert_outcomes(error=0, failed=0, passed=1)

    log_files = helpers.get_files_from_artifacts_dir_by_extension(testdir, "log")
    assert len(log_files) == 0
