import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_mark_examples.py"
    testdir.copy_example(filename)
    return filename


def test_single_arg_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::test_single_arg_in_mark"
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_labels = ["a_mark"]
    assert len(
        [record for record in json_records if record["labels"] == expected_labels]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_single_kwarg_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::test_single_kwarg_in_mark"
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_tags = {"my_mark": "a_mark"}
    assert len(
        [record for record in json_records if record["tags"] == expected_tags]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_multiple_args_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::test_multiple_args_in_mark"
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_labels = ["a_mark", "another_mark"]
    assert len(
        [record for record in json_records if record["labels"] == expected_labels]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_multiple_kwargs_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        f"{tests_filename}::test_multiple_kwargs_in_mark",
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_tags = {"my_mark": "a_mark", "my_other_mark": "another_mark"}
    assert len(
        [record for record in json_records if record["tags"] == expected_tags]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_with_single_arg_and_single_kwarg_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        f"{tests_filename}::test_with_args_and_kwargs_in_mark",
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_labels = ["a_mark"]
    assert len(
        [record for record in json_records if record["labels"] == expected_labels]
    ) == len(json_records)

    expected_tags = {"my_mark": "a_mark"}
    assert len(
        [record for record in json_records if record["tags"] == expected_tags]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_without_args_or_kwars_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::test_without_mark"
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_labels = None
    assert len(
        [record for record in json_records if record["labels"] == expected_labels]
    ) == len(json_records)

    expected_tags = None
    assert len(
        [record for record in json_records if record["tags"] == expected_tags]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)
