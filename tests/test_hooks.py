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

    expected_lines = [
        f'---> record: *, "when": "setup", *, "labels": [[]"{label}"[]]*',
        f'---> record: *, "when": "call", *, "labels": [[]"{label}"[]]*',
        f'---> record: *, "when": "teardown", *, "labels": [[]"{label}"[]]*',
    ]
    result.stdout.fnmatch_lines(expected_lines)


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

    expected_lines = [
        f'---> record: *, "when": "setup", *, "labels": [[]"a_mark", "{label}"[]]*',
        f'---> record: *, "when": "call", *, "labels": [[]"a_mark", "{label}"[]]*',
        f'---> record: *, "when": "teardown", *, "labels": [[]"a_mark", "{label}"[]]*',
    ]
    result.stdout.fnmatch_lines(expected_lines)


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

    expected_lines = [
        f'---> record: *, "when": "setup", *, "tags": {{"{tag_key}": "{tag_value}"}}*',
        f'---> record: *, "when": "call", *, "tags": {{"{tag_key}": "{tag_value}"}}*',
        f'---> record: *, "when": "teardown", *, "tags": {{"{tag_key}": "{tag_value}"}}*',
    ]
    result.stdout.fnmatch_lines(expected_lines)


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

    expected_lines = [
        f'---> record: *, "when": "setup", *, "tags": {{"my_mark": "a_mark", "{tag_key}": "{tag_value}"}}*',
        f'---> record: *, "when": "call", *, "tags": {{"my_mark": "a_mark", "{tag_key}": "{tag_value}"}}*',
        f'---> record: *, "when": "teardown", *, "tags": {{"my_mark": "a_mark", "{tag_key}": "{tag_value}"}}*',
    ]
    result.stdout.fnmatch_lines(expected_lines)
