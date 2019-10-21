import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_file_handling_tests.py"
    testdir.copy_example(filename)
    return filename


def test_single_json_file_is_created(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_files = helpers.get_files_from_artifacts_dir_by_extension(testdir, "json")
    assert len(json_files) == 1


def test_pickle_file_is_removed(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    pickle_files = helpers.get_files_from_artifacts_dir_by_extension(testdir, "pickle")
    assert len(pickle_files) == 0


def test_without_instrument_option(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest("-vs", f"{tests_filename}::{test_to_run}")
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_files = helpers.get_files_from_artifacts_dir_by_extension(testdir, "json")
    assert len(json_files) == 0
