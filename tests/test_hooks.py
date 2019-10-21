from tests import helpers


def test_label_hook_sets_first_label(testdir):
    tests_folder = "label_hook"
    tests_filename = "test_label_hook.py"
    test_to_run = "test_pass"
    label = "test"

    testdir.copy_example(tests_folder)
    result = testdir.runpytest(
        "-vs", "--instrument", f"--env={label}", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_json_file_from_artifacts_dir_and_return_records(testdir)
    expected_labels = [label]
    assert len(
        [record for record in records if record["labels"] == expected_labels]
    ) == len(records)


def test_label_hook_adds_label(testdir):
    tests_folder = "label_hook"
    tests_filename = "test_label_hook.py"
    test_to_run = "test_pass_with_label"
    label = "test"

    testdir.copy_example(tests_folder)
    result = testdir.runpytest(
        "-vs", "--instrument", f"--env={label}", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_json_file_from_artifacts_dir_and_return_records(testdir)
    expected_labels = ["a_mark", label]
    assert len(
        [record for record in records if record["labels"] == expected_labels]
    ) == len(records)


def test_tag_hook_sets_first_tag(testdir):
    tests_folder = "tag_hook"
    tests_filename = "test_tag_hook.py"
    test_to_run = "test_pass"
    tag_key = "env"
    tag_value = "test"

    testdir.copy_example(tests_folder)
    result = testdir.runpytest(
        "-vs",
        "--instrument",
        f"--{tag_key}={tag_value}",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_json_file_from_artifacts_dir_and_return_records(testdir)
    expected_tags = {tag_key: tag_value}
    assert len(
        [record for record in records if record["tags"] == expected_tags]
    ) == len(records)


def test_tag_hook_adds_tag(testdir):
    tests_folder = "tag_hook"
    tests_filename = "test_tag_hook.py"
    test_to_run = "test_pass_with_tag"
    tag_key = "env"
    tag_value = "test"

    testdir.copy_example(tests_folder)
    result = testdir.runpytest(
        "-vs",
        "--instrument",
        f"--{tag_key}={tag_value}",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_json_file_from_artifacts_dir_and_return_records(testdir)
    helpers.validate_json(records)

    expected_tags = {"my_mark": "a_mark", tag_key: tag_value}
    assert len(
        [record for record in records if record["tags"] == expected_tags]
    ) == len(records)


def test_fixture_hook_removes_fixture(testdir):
    tests_folder = "fixture_hook"
    tests_filename = "test_fixture_hook.py"
    test_to_run = "test_using_fixture"

    testdir.copy_example(tests_folder)
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(passed=1)

    records = helpers.get_json_file_from_artifacts_dir_and_return_records(testdir)
    helpers.validate_json(records)

    assert len([record for record in records if record["fixtures"] == []]) == len(
        records
    )
