import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_fixtures_examples.py"
    testdir.copy_example(filename)
    return filename


@pytest.mark.parametrize("fixture_scope", ["function", "module", "session"])
def test_setup_fixtures_with_different_scopes(testdir, tests_filename, fixture_scope):
    test_to_run = f"test_setup_fixture_{fixture_scope}_scope"
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_fixtures = [f"setup_fixture_with_{fixture_scope}_scope"]
    assert len(
        [record for record in json_records if record["fixtures"] == expected_fixtures]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


@pytest.mark.parametrize("fixture_scope", ["function", "module", "session"])
def test_teardown_fixtures_with_different_scopes(
    testdir, tests_filename, fixture_scope
):
    test_to_run = f"test_teardown_fixture_{fixture_scope}_scope"
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_fixtures = [f"teardown_fixture_with_{fixture_scope}_scope"]
    assert len(
        [record for record in json_records if record["fixtures"] == expected_fixtures]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_multiple_fixtures(testdir, tests_filename):
    test_to_run = "test_with_multiple_fixtures"
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_fixtures = [
        "setup_fixture_with_function_scope",
        "teardown_fixture_with_function_scope",
    ]
    assert len(
        [record for record in json_records if record["fixtures"] == expected_fixtures]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_without_fixtures(testdir, tests_filename):
    test_to_run = "test_with_no_fixtures"
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    assert len(
        [record for record in json_records if record["fixtures"] is None]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_named_fixture(testdir, tests_filename):
    test_to_run = "test_named_fixture"
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_fixtures = ["named_fixture"]
    assert len(
        [record for record in json_records if record["fixtures"] == expected_fixtures]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_child_fixture(testdir, tests_filename):
    test_to_run = "test_with_child_fixture"
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_fixtures = ["child_fixture", "parent_fixture"]
    assert len(
        [record for record in json_records if record["fixtures"] == expected_fixtures]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)
