from pathlib import PurePath
import re

import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_single_test_examples.py"
    testdir.copy_example(filename)
    return filename


def test_single_log_file_is_created_with_json_instrument_option(
    testdir, tests_filename
):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    log_files = helpers.get_files_from_artifacts_dir_by_extension(testdir, "log")
    assert len(log_files) == 1

    split_log_file_basename = PurePath(log_files[0]).stem.split("_", maxsplit=1)
    helpers.validate_timestamp(split_log_file_basename[0], "%Y%m%dT%H%M%S")

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    session_id = records[0]["session_id"]
    assert split_log_file_basename[1] == session_id[:8]


def test_single_log_file_is_created_with_log_instrument_option(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=log", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    log_files = helpers.get_files_from_artifacts_dir_by_extension(testdir, "log")
    assert len(log_files) == 1

    split_log_file_basename = PurePath(log_files[0]).stem.split("_", maxsplit=1)
    helpers.validate_timestamp(split_log_file_basename[0], "%Y%m%dT%H%M%S")

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    pattern = re.compile(r"^.+ session id: (.+)$")
    match = pattern.search(records[0])
    session_id = match[1]
    assert split_log_file_basename[1] == session_id[:8]


def test_no_file_created_without_instrument_option(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest("-vs", f"{tests_filename}::{test_to_run}")
    result.assert_outcomes(error=0, failed=0, passed=1)

    log_files = helpers.get_files_from_artifacts_dir_by_extension(testdir, "log")
    assert len(log_files) == 0
