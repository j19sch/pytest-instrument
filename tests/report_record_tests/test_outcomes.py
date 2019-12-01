import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_single_test_examples.py"
    testdir.copy_example(filename)
    return filename


def test_result_call_passes(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_when = "call"
    expected_outcome = "passed"
    assert (
        len(
            [
                record
                for record in records
                if record["when"] == expected_when
                and record["outcome"] == expected_outcome
            ]
        )
        == 1
    )


def test_result_call_fails(testdir, tests_filename):
    test_to_run = "test_fails"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=1, passed=0)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_when = "call"
    expected_outcome = "failed"
    assert (
        len(
            [
                record
                for record in records
                if record["when"] == expected_when
                and record["outcome"] == expected_outcome
            ]
        )
        == 1
    )


def test_result_setup_passes(testdir, tests_filename):
    test_to_run = "test_setup_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_when = "setup"
    expected_outcome = "passed"
    assert (
        len(
            [
                record
                for record in records
                if record["when"] == expected_when
                and record["outcome"] == expected_outcome
            ]
        )
        == 1
    )


def test_result_setup_fails(testdir, tests_filename):
    test_to_run = "test_setup_fails"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=1, failed=0, passed=0)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_when = "setup"
    expected_outcome = "failed"
    assert (
        len(
            [
                record
                for record in records
                if record["when"] == expected_when
                and record["outcome"] == expected_outcome
            ]
        )
        == 1
    )


def test_result_teardown_passes(testdir, tests_filename):
    test_to_run = "test_teardown_passes"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_when = "teardown"
    expected_outcome = "passed"
    assert (
        len(
            [
                record
                for record in records
                if record["when"] == expected_when
                and record["outcome"] == expected_outcome
            ]
        )
        == 1
    )


def test_result_teardown_fails(testdir, tests_filename):
    test_to_run = "test_teardown_fails"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=1, failed=0, passed=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_when = "teardown"
    expected_outcome = "failed"
    assert (
        len(
            [
                record
                for record in records
                if record["when"] == expected_when
                and record["outcome"] == expected_outcome
            ]
        )
        == 1
    )


def test_result_setup_and_teardown_fail(testdir, tests_filename):
    test_to_run = "test_setup_and_teardown_fail"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=1, failed=0, passed=0)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_when = "setup"
    expected_outcome = "failed"
    assert (
        len(
            [
                record
                for record in records
                if record["when"] == expected_when
                and record["outcome"] == expected_outcome
            ]
        )
        == 1
    )

    expected_when = "call"
    assert len([record for record in records if record["when"] == expected_when]) == 0

    expected_when = "teardown"
    expected_outcome = "passed"
    assert (
        len(
            [
                record
                for record in records
                if record["when"] == expected_when
                and record["outcome"] == expected_outcome
            ]
        )
        == 1
    )


def test_result_skipped(testdir, tests_filename):
    test_to_run = "test_skipped"
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=0, skipped=1)

    records = helpers.get_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_when = "setup"
    expected_outcome = "skipped"
    assert (
        len(
            [
                record
                for record in records
                if record["when"] == expected_when
                and record["outcome"] == expected_outcome
            ]
        )
        == 1
    )

    expected_when = "call"
    assert len([record for record in records if record["when"] == expected_when]) == 0

    expected_when = "teardown"
    expected_outcome = "passed"
    assert (
        len(
            [
                record
                for record in records
                if record["when"] == expected_when
                and record["outcome"] == expected_outcome
            ]
        )
        == 1
    )
