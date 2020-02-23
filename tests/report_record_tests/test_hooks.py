from tests import helpers


def test_label_hook_sets_first_label(testdir):
    tests_folder = "label_hook"
    tests_filename = "test_label_hook_examples.py"
    test_to_run = "test_pass"
    label = "test"

    testdir.copy_example(tests_folder)
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        f"--env={label}",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_labels = [label]
    assert len(
        [record for record in json_records if record["labels"] == expected_labels]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_label_hook_adds_label(testdir):
    tests_folder = "label_hook"
    tests_filename = "test_label_hook_examples.py"
    test_to_run = "test_pass_with_label"
    label = "test"

    testdir.copy_example(tests_folder)
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        f"--env={label}",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_labels = ["a_mark", label]
    assert len(
        [record for record in json_records if record["labels"] == expected_labels]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_tag_hook_sets_first_tag(testdir):
    tests_folder = "tag_hook"
    tests_filename = "test_tag_hook_examples.py"
    test_to_run = "test_pass"
    tag_key = "env"
    tag_value = "test"

    testdir.copy_example(tests_folder)
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        f"--{tag_key}={tag_value}",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_tags = {tag_key: tag_value}
    assert len(
        [record for record in json_records if record["tags"] == expected_tags]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_tag_hook_adds_tag(testdir):
    tests_folder = "tag_hook"
    tests_filename = "test_tag_hook_examples.py"
    test_to_run = "test_pass_with_tag"
    tag_key = "env"
    tag_value = "test"

    testdir.copy_example(tests_folder)
    result = testdir.runpytest(
        "-vs",
        "--instrument=json,log",
        f"--{tag_key}={tag_value}",
        f"{tests_filename}::{test_to_run}",
    )
    result.assert_outcomes(passed=1)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    helpers.json_validate_each_record(json_records)

    expected_tags = {"my_mark": "a_mark", tag_key: tag_value}
    assert len(
        [record for record in json_records if record["tags"] == expected_tags]
    ) == len(json_records)

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)


def test_fixture_hook_removes_fixture(testdir):
    tests_folder = "fixture_hook"
    tests_filename = "test_fixture_hook_examples.py"
    test_to_run = "test_using_fixture"

    testdir.copy_example(tests_folder)
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(passed=1)

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
