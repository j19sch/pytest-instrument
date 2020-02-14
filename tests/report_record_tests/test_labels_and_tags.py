import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_mark_examples.py"
    testdir.copy_example(filename)
    return filename


def test_single_arg_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::test_single_arg_in_mark"
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_labels = ["a_mark"]
    assert len(
        [record for record in records if record["labels"] == expected_labels]
    ) == len(records)


def test_single_kwarg_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::test_single_kwarg_in_mark"
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_tags = {"my_mark": "a_mark"}
    assert len(
        [record for record in records if record["tags"] == expected_tags]
    ) == len(records)


def test_multiple_args_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::test_multiple_args_in_mark"
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_labels = ["a_mark", "another_mark"]
    assert len(
        [record for record in records if record["labels"] == expected_labels]
    ) == len(records)


def test_multiple_kwargs_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::test_multiple_kwargs_in_mark"
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_tags = {"my_mark": "a_mark", "my_other_mark": "another_mark"}
    assert len(
        [record for record in records if record["tags"] == expected_tags]
    ) == len(records)


def test_with_single_arg_and_single_kwarg_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs",
        "--instrument=json",
        f"{tests_filename}::test_with_args_and_kwargs_in_mark",
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_labels = ["a_mark"]
    assert len(
        [record for record in records if record["labels"] == expected_labels]
    ) == len(records)

    expected_tags = {"my_mark": "a_mark"}
    assert len(
        [record for record in records if record["tags"] == expected_tags]
    ) == len(records)


def test_without_args_or_kwars_in_mark_instrument(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument=json", f"{tests_filename}::test_without_mark"
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    helpers.json_validate_each_record(records)

    expected_labels = None
    assert len(
        [record for record in records if record["labels"] == expected_labels]
    ) == len(records)

    expected_tags = None
    assert len(
        [record for record in records if record["tags"] == expected_tags]
    ) == len(records)
