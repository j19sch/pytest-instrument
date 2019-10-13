import pytest


# setup and teardown
# fixture scope
# nested fixtures


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_fixtures_tests.py"
    testdir.copy_example(filename)
    return filename


@pytest.mark.parametrize("fixture_scope", ["function", "module", "session"])
def test_setup_fixtures_with_different_scopes(testdir, tests_filename, fixture_scope):
    test_to_run = f"test_setup_fixture_{fixture_scope}_scope"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    result.stdout.fnmatch_lines(
        f'---> record: *, "fixtures": [[]"setup_fixture_with_{fixture_scope}_scope"[]]*'
    )


@pytest.mark.parametrize("fixture_scope", ["function", "module", "session"])
def test_teardown_fixtures_with_different_scopes(
    testdir, tests_filename, fixture_scope
):
    test_to_run = f"test_teardown_fixture_{fixture_scope}_scope"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    result.stdout.fnmatch_lines(
        f'---> record: *, "fixtures": [[]"teardown_fixture_with_{fixture_scope}_scope"[]]*'
    )


def test_multiple_fixtures(testdir, tests_filename):
    test_to_run = "test_with_multiple_fixtures"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    result.stdout.fnmatch_lines(
        '---> record: *, "fixtures": [[]"setup_fixture_with_function_scope", "teardown_fixture_with_function_scope"[]]*'
    )


def test_without_fixtures(testdir, tests_filename):
    test_to_run = "test_with_no_fixtures"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    result.stdout.fnmatch_lines('---> record: *, "fixtures": [[][]]*')


def test_named_fixture(testdir, tests_filename):
    test_to_run = "test_named_fixture"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    result.stdout.fnmatch_lines('---> record: *, "fixtures": [[]"named_fixture"[]]*')


def test_child_fixture(testdir, tests_filename):
    test_to_run = "test_with_child_fixture"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    result.stdout.fnmatch_lines(
        '---> record: *, "fixtures": [[]"child_fixture", "parent_fixture"[]]*'
    )
